CREATE TABLE IF NOT EXISTS anomalies (ID serial PRIMARY KEY, diseases text, category text, response text, scientific_name text);

INSERT INTO anomalies (diseases, category, response, scientific_name) VALUES ('Healthy', 'Disease', 'Congratulations! Your crops are in good condition.', 'Healthy');
INSERT INTO anomalies (diseases, category, response, scientific_name) VALUES ('Leaf Blast', 'Disease', 'Your crops have been infected by the rice blast fungus!', 'Magnaporthe oryzae');
INSERT INTO anomalies (diseases, category, response, scientific_name) VALUES ('Brown Spot', 'Disease', 'We have detected brown spots on your crops!', 'Cochliobolus miyabeanus');
INSERT INTO anomalies (diseases, category, response, scientific_name) VALUES ('Hispa', 'Disease', 'We have found traces of rice hispa within your crops!', 'Dicladispa armigera');

CREATE TABLE IF NOT EXISTS causes (ID serial PRIMARY KEY, diseases text, cause text, anomalies_ID integer REFERENCES anomalies (ID));

INSERT INTO causes (diseases, cause) VALUES ('Healthy', 'Normal');
INSERT INTO causes (diseases, cause) VALUES ('LeafBlast', 'Infection rice blast fungus (Pyricularia grisea.), infection can come from seeds, diseased plant residues or grasses around plants. This also can causes from lack of kalium (Potassium) and silica, lack of water and plant stress due to herbicides.');
INSERT INTO causes (diseases, cause) VALUES ('BrownSpot', 'Brown leaf spot disease on rice (Oryza sativa l) is caused by the fungus Helminthosporium oryzae or Drechslera oryzae (Cochliobolus miyabeanus). The conidia of H. Oryzae are brown, 6-17 insulated, cylindrical in shape, slightly curved, and slightly widened in the middle.This can also occur due to host conditions that are suitable for the initiation of brown spots, such as cloudy conditions, rain, dew with temperatures between 20-29 c.');
INSERT INTO causes (diseases, cause) VALUES ('Hispa', 'Adult insects and larvae of the rice hispa Dicladispa armigera. Insects erode the upper surface of the leaf and leave the lower epidermis and lay their eggs in small crevices on the leaf, usually at the tip of the leaf.');

CREATE TABLE IF NOT EXISTS cures (ID serial PRIMARY KEY, diseases text, cure text, anomalies_ID integer REFERENCES anomalies (ID));

INSERT INTO cures (diseases, cure)  VALUES ('Healthy', 'Normal');
INSERT INTO cures (diseases, cure) VALUES ('LeafBlast', 'Apply fungicides by spraying on plants (Benomyl 50WP, Mancozeb 80%, Carbendazim 50%, isoprotiolan 40%, and trisikazole 20%). Provide a balanced nutrition to the rice crop. Increase the use manure, green manure or compost. Increase potassium levels using artificial fertilizers such as KCl, as well as wood fire ash, rubbing ash, husk ash.');
INSERT INTO cures (diseases, cure) VALUES ('BrownSpot', 'Apply fungicides by spraying on plants (Rabcide 50 WP, score, anvil, folicur, Nativo, opus, indar). Spraying fungicides with the active ingredients diphenoconazole, azoxistrobin, sulfur, diphenoconazole, caneconazole, carbendazim, methyl thiophanate or chlorotalonyl. Provide a balanced nutrition to the rice crop.');
INSERT INTO cures (diseases, cure) VALUES ('Hispa', 'Avoid excessive nitrogen fertilization. Affected leaves should be cut and burned, or buried. Use a net to catch insects, do it in the morning when they are less mobile. Provision of natural enemies, such as small wasps that can attack eggs and larvae, or reduviid insects to eat adults insects. Apply active ingredients or insecticides (chlorpyrifos, malathion, spermethrin, fentoate. You can also use environmentally friendly vegetable pesticides such as neem leaves, tuba roots, jengkol, etc');

CREATE TABLE IF NOT EXISTS preventions (ID serial PRIMARY KEY, diseases text, prevention text, anomalies_ID integer REFERENCES anomalies (ID));

INSERT INTO preventions (diseases, prevention) VALUES ('Healthy', 'Normal');
INSERT INTO preventions (diseases, prevention) VALUES ('LeafBlast', 'Use certified seed and resistance (Inpari 21, Inpari 22, Inpari 26, Inpari 27, Inpago 4, Inpago 5, Inpago 6, Inpago 7, dan Inpago 8). Pretreat your seed with hot water or fungicides. Carry out crop rotation or intercropping. Actively manage weeds. Avoid the use of herbicides, as they increase susceptibility to blast. Modify plant density so to avoid close spacing since this favors warm and humid conditions ideal for blast.');
INSERT INTO preventions (diseases, prevention) VALUES ('BrownSpot', 'Use certified seed and resistance (Ciherang dan Membrano. Complete balanced fertilization, namely 250 kg urea, 100 kg SP36, and 100 kg KCl per ha). Spacing is not too close, especially during the rainy season. Actively manage weeds.');
INSERT INTO preventions (diseases, prevention) VALUES ('Hispa', 'Do crop rotation. Clean weeds regularly. Cut the tip of the leaf. Plant early in the season to avoid peak population. Use closer spacing.');

CREATE TABLE IF NOT EXISTS resources (ID serial PRIMARY KEY, diseases text, resource text, anomalies_ID integer REFERENCES anomalies (ID));

INSERT INTO resources (diseases, resource) VALUES ('Healthy', 'Normal');
INSERT INTO resources (diseases, resource) VALUES ('LeafBlast', 'https://wiki.bugwood.org/Magnaporthe_oryzae, https://bbpadi.litbang.pertanian.go.id/index.php/info-berita/info-teknologi/penyakit-blas-pada-tanaman-padi-dan-cara-pengendaliannya, https://ptn.ipb.ac.id/cms/id/berita/detail/251/seri-dokter-tanaman-ipb-mengatasi-penyakit-blas-pada-padi');
INSERT INTO resources (diseases, resource) VALUES ('BrownSpot', 'http://cybex.pertanian.go.id/artikel/90421/penyakit-bercak-daun-pada-tanaman-padi/');
INSERT INTO resources (diseases, resource) VALUES ('Hispa', 'https://plantix.net/id/library/plant-diseases/600098/rice-hispa');
