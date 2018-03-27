#!/usr/bin/env python

import spacy
nlp = spacy.load("en")
doc = nlp("The big grey dog ate all of the chocolate, but fortunately he wasn't sick!")
