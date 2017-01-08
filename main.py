# -*- coding: utf-8 -*-
from __future__ import division
import os
from nltk.corpus import stopwords
import re
from math import log


cached_stoppper_words = stopwords.words("english")
positive_word_dict = {}
negative_word_dict = {}
total_word_set = set()
probability_dict = {}
total_word_count = 0
probability_of_pos_class= {}
probability_of_neg_class = {}

def extract_positive_words():
    #Open directory containing positive reviews
    positive_reviews_path = "LargeIMDB/pos//"
    positive_listing = os.listdir(positive_reviews_path)
    
    global positive_word_dict
    global total_word_count
    #Iterate each_file and extract each word for positive reviews
    for each_file in positive_listing:
        print each_file
        #print "Current file is:", each_file
        current_file = open(positive_reviews_path+each_file, "r")
        
        #Read contents of file and lower case all words
        content = current_file.read().lower()
        
        #Remove all non lower case letters from content and replace with blank space
        content = re.sub('[^a-z]', ' ', content)
        current_file.close()
        
        #Remove all blank spaces
        words = content.split()
        #Add words to dictionary
        for word in words:
            total_word_set.add(word)
            if word in positive_word_dict:
                positive_word_dict[word] += 1
            else:
                positive_word_dict[word] = 1
  
def extract_negative_words():
    #Open directory containing negative reviews
    negative_reviews_path = "LargeIMDB/neg//"
    negative_listing = os.listdir(negative_reviews_path)
    
    global total_word_count    
    
    global negative_word_dict
    
    #Iterate each_file and extract each word for negative reviews
    for each_file in negative_listing:
        print each_file
        #print "Current file is:", each_file
        current_file = open(negative_reviews_path+each_file, "r")
        
        #Read contents of file and lower case all words
        content = current_file.read().lower()
        
        #Remove all non lower case letters from content and replace with blank space
        content = re.sub('[^a-z]', ' ', content)
        current_file.close()
        
        #Remove all blank spaces
        words = content.split()
        #Add words to dictionary
        for word in words: 
            total_word_set.add(word)
            if word in negative_word_dict:
                negative_word_dict[word] += 1
            else:
                negative_word_dict[word] = 1

 
def remove_stopper_words():
    for word in cached_stoppper_words:
        if word in total_word_set:
            total_word_set.remove(word)
        if word in negative_word_dict:
            del negative_word_dict[word]
        if word in positive_word_dict:
            del positive_word_dict[word]
      
def calculate_probability():
    #Probability of class
    total_word_count = 0
    global total_files
    for word in total_word_set:
        if word not in positive_word_dict:
            positive_word_dict[word] = 0
        if word not in negative_word_dict:
            negative_word_dict[word] = 0
            
    for word in total_word_set:
        total_word_count = total_word_count + positive_word_dict[word]
        total_word_count = total_word_count + negative_word_dict[word]
        
    print "total_word_dict", len(total_word_set)  
    print "positive_word_dict", len(positive_word_dict)  
    print "negative_word_dict", len(negative_word_dict)  
    for word in total_word_set:   
        #Use for smoothing add total word count to total unique words
        probability_of_pos_class[word] = ((positive_word_dict[word] + 1) / (len(total_word_set) + total_word_count))
        probability_of_neg_class[word] = ((negative_word_dict[word] + 1) / (len(total_word_set) + total_word_count))
    print probability_of_pos_class[word]
    print probability_of_pos_class[word]

def classifier():
    #Open directory containing negative reviews
    listOfFolder = ["smallTest/pos//", "smallTest/neg//"]

    for path in listOfFolder:
        print path
        total_postive = 0
        total_negitive = 0
        number_of_text_files = 0
        listing = os.listdir(path)
        
        #Iterate each_file and extract each word for negative reviews
        for each_file in listing:
            postive = 0
            negitive = 0
            #print "Current file is:", each_file
            current_file = open(path+each_file, "r")
            
            #Read contents of file and lower case all words
            content = current_file.read().lower()
            
            #Remove all non lower case letters from content and replace with blank space
            content = re.sub('[^a-z]', ' ', content)
            current_file.close()
            
            #Remove all blank spaces
            words = content.split()
            for word in words: 
                if word in total_word_set:
                    postive += log(float(probability_of_pos_class[word])) 
                    negitive += log(float(probability_of_neg_class[word]))
            number_of_text_files +=1
            if postive > negitive:
                total_postive += 1
            else:
               total_negitive +=1
        print "Postive: ", (float(total_postive)/float(number_of_text_files)), "%"
        print "Negitive: ", (float(total_negitive)/float(number_of_text_files)), "%"            
         
extract_positive_words()
extract_negative_words()
remove_stopper_words()
calculate_probability()
classifier()