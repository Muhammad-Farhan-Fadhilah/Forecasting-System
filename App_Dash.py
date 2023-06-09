import datetime
import pandas as pd

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

from PIL import Image
import io
import base64

import torch
import torch.nn as nn

import torchvision.models as models
import torchvision.transforms as T

model_path = r'resnet101_model_best_checkpoint.pth'

load = torch.load(model_path, map_location=torch.device('cpu'))
if torch.cuda.is_available():
    load = torch.load(model_path, map_location=torch.device('cuda'))

model = models.resnet101(pretrained=True)
num_ftrs = model.fc.in_features
number_of_classes = 4
model.fc = nn.Linear(num_ftrs, number_of_classes)
model.load_state_dict(load['model'])

classes = ['BrownSpot', 'Healthy', 'Hispa', 'LeafBlast']
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

image_transforms = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(torch.Tensor(mean), torch.Tensor(std))
])

# web app
styleCss = ['assets/style.css']
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Img(src=logo_path, className='logo-image'),
                html.H1(children='Rice Disease Detection', className='logo-title')
                ], className='logo'),
            html.Div(id='output-image-upload', children='')],
            className='contents-upload'),
        html.Div([
            dcc.Upload(id='upload-image',
                       children=html.Div(['Drag and Drop or ', html.A('Select Files')], className='upload-image'),
                       multiple=True),
            html.Div([
                html.H3(children='Content-Info', className='content-title'),
                html.Div(id='output-filename-upload', children='', className='content-info'),
                html.Div(id='output-date-upload', children='', className='content-info'),
                html.Div([
                    html.H3(children='Prediction', className='prediction-title'),
                    html.Div(id='output-prediction-upload', children='', className='prediction-content')],
                    className='prediction-dropdown')],
                className='image-info'),
            html.Div([
                html.Div([
                    html.H3(children='Response', className='box-title'),
                    html.Div(id='output-response', children='', className='box-info')],
                    className='box-dropdown'),
                html.Div([
                    html.H3(children='Category', className='box-title'),
                    html.Div(id='output-category', children='', className='box-info')],
                    className='box-dropdown'),
                html.Div([
                    html.H3(children='Scientific Name', className='box-title'),
                    html.Div(id='output-scientific-name', children='', className='box-info')],
                    className='box-dropdown'),
                html.Div([
                    html.H3(children='Cause', className='box-title'),
                    html.Div(id='output-cause', children='', className='box-info')],
                    className='box-dropdown'),
                html.Div([
                    html.H3(children='Cure', className='box-title'),
                    html.Div(id='output-cure', children='', className='box-info')],
                    className='box-dropdown'),
                html.Div([
                    html.H3(children='Prevention', className='box-title'),
                    html.Div(id='output-prevention', children='', className='box-info')],
                    className='box-dropdown'),
                html.Div([
                    html.H3(children='Resources', className='box-title'),
                    html.Div(id='output-resource', children='', className='box-info')],
                    className='box-dropdown')],
                className='recomendation-info')],
            className='sidebar')],
        className='app-container')],
    className='app-body')

# access data from the storage or csv to dataframe
def access_anomalies():
    path = 'anomalies/anomalies.csv'
    data = pd.read_csv(path, sep=';')
    return data

def access_cause():
    path = 'anomalies/causes.csv'
    data = pd.read_csv(path, sep=';')
    return data

def access_cure():
    path = 'anomalies/cure.csv'
    data = pd.read_csv(path, sep=';')
    return data

def access_prevention():
    path = 'anomalies/prevention.csv'
    data = pd.read_csv(path, sep=';')
    return data

def access_resource():
    path = 'anomalies/resource.csv'
    data = pd.read_csv(path, sep=';')
    return data

def resource_extract(ID):
    resource = access_resource()
    resource = resource[resource['ID'] == ID.item()]['resource']
    return resource

def prevention_extract(ID):
    prevention = access_prevention()
    preventions = prevention[prevention['ID'] == ID.item()]['prevention']
    return preventions

def cure_extract(ID):
    cure = access_cure()
    cures = cure[cure['ID'] == ID.item()]['cure']
    return cures

def cause_extract(ID):
    cause = access_cause()
    causes = cause[cause['ID'] == ID.item()]['causes']
    return causes

# Merge the result with combined data
def id_extract_anomalies(result):
    #load all datas
    anomalies = access_anomalies()
    #parse the correct data
    anomalies = anomalies[anomalies['anomalies'] == result]
    ID = anomalies[anomalies['anomalies'] == result]['ID']
    category = anomalies[anomalies['anomalies'] == result]['category']
    response = anomalies[anomalies['anomalies'] == result]['response']
    scientific_name = anomalies[anomalies['anomalies'] == result]['scientific_name']
    return ID, category, response, scientific_name


# classification
def classify(image):
    model.eval()
    if torch.cuda.is_available():
        model.cuda()
    image = image_transforms(image)
    if torch.cuda.is_available():
        image = image.cuda()
    image = image.unsqueeze(0)
    output = model(image)
    _, predicted = torch.max(output.data, 1)
    return classes[predicted.item()]

# visualization

predictions = []
categories = []
responses = []
names = []
causes = []
cures = []
preventions = []
resources = []

@app.callback(Output('output-image-upload', 'children'),
              Output('output-filename-upload', 'children'),
              Output('output-date-upload', 'children'),
              Output('output-prediction-upload', 'children'),
              Output('output-response', 'children'),
              Output('output-category', 'children'),
              Output('output-scientific-name', 'children'),
              Output('output-cause', 'children'),
              Output('output-cure', 'children'),
              Output('output-prevention', 'children'),
              Output('output-resource', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    prediction = 'Healthy'
    if list_of_contents is None:
        raise PreventUpdate
    else:
        # processing uploaded image
        for i in list_of_contents:
            #Restore Image
            # extract the pixel code
            encoded_image = i.split(",")[1] # the crucial part of decode base64.
            # decoding from base64
            decoded_image = base64.b64decode(encoded_image)
            bytes_image = io.BytesIO(decoded_image)

            image = Image.open(bytes_image).convert('RGB')
            prediction = str(classify(image))

            #catch
            existing_df = pd.read_csv('storage/save.csv')
            new_row = {'image': i, 'text': prediction}
            existing_df = existing_df.append(new_row, ignore_index=True)
            existing_df.to_csv('storage/save.csv', index=False)


            print('the prediction:' + prediction)
            re = ''
            if prediction != 'Healthy':
                predictions.append(prediction)
                for i in predictions:
                    print('The Predictions: '+i)
                print('result of prediction: '+prediction)
                ID, category, response, scientific_name = id_extract_anomalies(prediction)
                print('The ID: ' + str(ID))
                print('The Category:' + str(category))
                re = response

                print('The Response: ' + str(response))
                print('The Scientific Name: ' + str(scientific_name))
                categories.append(category)
                responses.append(response)
                names.append(scientific_name)

                cause = cause_extract(ID)
                print('The Cause: ' + str(cause))
                causes.append(cause)

                cure = cure_extract(ID)
                print('The Cure: '+ cure)
                cures.append(cure)

                prevention = prevention_extract(ID)
                print('The Prevention: '+prevention)
                preventions.append(prevention)

                resource = resource_extract(ID)
                print('The Resource: '+resource)
                resources.append(resource_extract(ID))

            else:
                predictions.append(prediction)
                for i in predictions:
                    print('The Predictions: '+i)
                print('result of prediction: '+prediction)
                ID, category, response, scientific_name = id_extract_anomalies(prediction)
                re = response
                print('The ID: ' + str(ID))
                print('The Category:' + str(category))
                print('The Response: ' + str(response))
                print('The Scientific Name: ' + str(scientific_name))
                responses.append(response)

        img = html.Div()
        filename = html.H5()
        date = html.H6()
        pred = html.H5()
        category = html.H5()
        name = html.H5()
        cause = html.H5()
        cure = html.H5()
        prevention = html.H5()
        resource = html.H5()
        print("html results declared")

        if prediction == 'Healthy':
            print('Compared Variable for html parser: '+prediction)
            for c, n, p, d, r in zip(list_of_contents, list_of_names, predictions, list_of_dates, responses):
                img = html.Img(src=c)
                filename = html.H5(n)
                date = html.H6(datetime.datetime.fromtimestamp(d))
                pred = html.H5(prediction)
                print('html parser for healthy: '+prediction)
                response = html.H5(re)
                print('html parser of response' + re)
                category = html.H5('')
                name = html.H5('')
                cause = html.H5('')
                cure = html.H5('')
                prevention = html.H5('')
                resource = html.H5('')

            return img, filename, date, pred, response, category, name, cause, cure, prevention, resource

        else:
            print('Compared Variable for html parser: '+prediction)
            for con, fn, p, d, r, cat, na, cau, cu, pre, res  in zip(list_of_contents, list_of_names, predictions, list_of_dates, responses, categories, names, causes, cures, preventions, resources):
                img = html.Img(src=con)
                filename = html.H5(fn)
                date = html.H6(datetime.datetime.fromtimestamp(d))
                pred = html.H5(prediction)
                print('html parser for non healthy: '+prediction)
                response = html.H5(re)
                print('html parser of response' + re)
                category = html.H5(cat)
                name = html.H5(na)

                cause = html.H5(cau)
                if len(cau) > 1:
                    cause = parse_content(cau)

                cure = html.H5(cu)
                if len(cu) > 1:
                    cure = parse_content(cu)

                prevention = html.H5(pre)
                if len(pre) > 1:
                    prevention = parse_content(pre)

                resource = html.H5(res)
                if len(res) > 1:
                    resource = parse_content(res)

            return img, filename, date, pred, response, category, name, cause, cure, prevention, resource

def parse_content(source):
    content = [html.Div(html.H5(i),
                                     style={
                                        'border-width': '1px',
                                        'border-style': 'outset',
                                        'border-radius': '5px',
                                        'margin': '10px auto',
                                        'padding': '0 2px 2px 5px',
                                        'background-color': 'cornsilk'
                                     }) for i in source]
    return content

if __name__ == '__main__':
    app.run_server(debug=True)