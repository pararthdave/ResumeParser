# -*- coding: utf-8 -*-
#importing libraries
import nltk
import re
from datetime import datetime
from dateutil.rrule import rrule, MONTHLY
import spacy
from nltk.corpus import stopwords
nlp = spacy.load('en_core_web_sm')
import pandas as pd
import pdftotext
from spacy.matcher import  Matcher, PhraseMatcher
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import locationtagger
nltk.downloader.download('maxent_ne_chunker')
nltk.downloader.download('words')
nltk.downloader.download('treebank')
nltk.downloader.download('maxent_treebank_pos_tagger')
nltk.downloader.download('punkt')
nltk.download('averaged_perceptron_tagger')



class ResumeParser:
  def split(delimiters, string, maxsplit=0):
    import re
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)
  def get_lang_list():
    filePath = 'Languages.csv'
    df = pd.read_csv(filePath)
    # str.replace('; ', ', ') and then a str.split(', ')
    df['Language name '].replace(to_replace ="marathi (marāṭhī)",
                 value ="marathi")
    # languages = df.iloc[:, [3]].to_list()
    lang_list =df['Language name '].to_list()
    all_lang_list=[]
    for i in lang_list:
        i=i.strip().lower()
        i = ResumeParser.split(' ,;()', i)
        if(type(i) == list):
            for x in i:
                if(x!=''):
                    all_lang_list.append(x)
        else:
            all_lang_list.append(i)
    wordsToRemove = ["standard", "central", "modern"]
    for word in wordsToRemove:
        all_lang_list.remove(word)
    
    return all_lang_list
  def extract_language(self, input_text):
    languages = ResumeParser.get_lang_list()
    # print(languages)
    nlp_text = nlp(input_text)
    noun_chunks = nlp_text.noun_chunks
    # print(type(noun_chunks))
    tokens = [token.text for token in nlp_text if not token.is_stop]
    master_language = []


    for token in tokens:
        if token.lower() in languages:
            master_language.append(token)
    
    for token in noun_chunks:
        token = token.text.lower().strip()
        # print(token)
        for lang in languages:
            if(token==lang):
                master_language.append(token)
            # if(lang.find(token) != -1):
            #     master_language.append(token)

        # if token in languages:
        #     master_language.append(token)
    return [i.capitalize() for i in set([i.lower() for i in master_language])]

  
  def locationExtraction(self, text):
    text = text.title()
    place_entity = locationtagger.find_locations(text = text)
    ans = (place_entity.country_cities)
    
    if "India" in ans:
      gpe = (ans['India'])
    else:
      gpe = "No location found"

    return gpe
  def extract_text(self,resume_text):
    nlp = spacy.load('en_core_web_sm')
    STOPWORDS = set(stopwords.words('english'))
    Education = ['BE','B.E.', 'B.E', 'BS', 'B.S', 
              'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
              'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
              'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII']


    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in Education and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education
  def extract_experience(self,pdf_text):
    # Create sentance tokens from the text
    lines = [el.strip() for el in pdf_text.split("\n") if len(el) > 0]
    # Create word tokens from sentances
    lines = [nltk.word_tokenize(el) for el in lines]
    # Assign "Part of Speech" tags to each word
    lines = [nltk.pos_tag(el) for el in lines]


    # Capture sentances which contain the term "Experience" and "Education"

    for sentance in lines:
      # Discard tags from words and join all words
      sen = " ".join([words[0].lower() for words in sentance])


      if re.search('experience',sen):
        sen_tokenised = nltk.word_tokenize(sen)
        tagged = nltk.pos_tag(sen_tokenised)
        # Create chunks of data using the recommended named entity chunker
        entities = nltk.chunk.ne_chunk(tagged)
        for subtree in entities.subtrees():
          for leaf in subtree.leaves():
            if leaf[1] == 'CD':
              # Extract Date from that sentance
              experience = leaf[0]
      if re.search('education',sen):
        sen_tokenised = nltk.word_tokenize(sen)
        tagged = nltk.pos_tag(sen_tokenised)
        entities = nltk.chunk.ne_chunk(tagged)
        for subtree in entities.subtrees():
          for leaf in subtree.leaves():
            if leaf[1] == 'CD':
              # Extract Date from that sentance
              education = leaf[0]

    # Convert the dates to DateTime objects
    date_time_obj_edu = datetime.strptime(education, '%d/%m/%Y')
    date_time_obj_exp = datetime.strptime(experience, '%d/%m/%Y')

    # Get number of months between the two dates
    strt_dt = date_time_obj_edu
    end_dt = date_time_obj_exp
    dates = [dt for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]

    # Return experience as number of months
    print ("Experience in Months: ")
    return (len(dates) - 1)
  # loading pretrained model

  def extract_skills(self,pdf_text):
    temp="""java
    javascript 
    html
    python
    c
    c++
    angular js
    reactjs
    golang
    data analytics
    sql
    mysql
    nosql
    data science
    machine learning
    bootstrap
    vscode
    pycharm
    web development
    skLearn
    Keras
    spaCY
    Communication
    Leadership
    Management
    Creativity
    Team Work
    Problem Solving
    SAS Certified Specialist: Base Programming Using
    css"""

    nlp_text=nlp(pdf_text)

    tokens = [token.text for token in nlp_text if not token.is_stop]
    for j,i in enumerate(tokens):
      if i.lower()=='skills':
        j+=1
        x=tokens[j]
        ans=''
        while (j<len(tokens) or x!='\n'):
          if (nlp(x)[0].pos_ in ['NOUN','VERB'] or x.lower() in temp.lower()):
            ans=ans+x+' '
            if x=='\n':
              break
            if j<len(tokens) and nlp(tokens[j])[0].pos_ == 'SPACE':
              j+=1
            if x=='\n':
              break
            if (nlp(x)[0].pos_=='NOUN' or nlp(x)[0].pos_=='VERB') and j<len(tokens) and nlp(tokens[j])[0].pos_ not in ['NOUN','SPACE','PUNCT']:
              ans=ans+ ','
          j+=1
          if j>=len(tokens) or x=='\n':
            break
          x=tokens[j]
        ans=ans.replace(' ,',',')
        #print(ans)
        
        break

    return ans

  def extract_hobby(self, resume_text):
    temp = """3D printing
    Acting
    Writing
    Aeromodeling
    Air sports
    Airbrushing
    Aircraft Spotting
    Airsoft
    Airsofting
    Amateur astronomy
    Amateur geology
    Amateur Radio
    American football
    Animal fancy
    Animals/pets/dogs
    Antiquing
    Antiquities
    Aqua-lung
    Aquarium (Freshwater & Saltwater)
    Archery
    Art collecting
    Arts
    Association football
    Astrology
    Astronomy
    Audiophilia
    Australian rules football
    Auto audiophilia
    Auto racing
    Backgammon
    Backpacking
    Badminton
    Base Jumping
    Baseball
    Basketball
    Baton Twirling
    Beach Volleyball
    Beach/Sun tanning
    Beachcombing
    Beadwork
    Beatboxing
    Becoming A Child Advocate
    Beekeeping
    Bell Ringing
    Belly Dancing
    Bicycle Polo
    Bicycling
    Billiards
    Bird watching
    Birding
    Birdwatching
    Blacksmithing
    Blogging
    BMX
    Board games
    Board sports
    BoardGames
    Boating
    Body Building
    Bodybuilding
    Bonsai Tree
    Book collecting
    Bookbinding
    Boomerangs
    Bowling
    Boxing
    Brazilian jiu-jitsu
    Breakdancing
    Brewing Beer
    Bridge
    Bridge Building
    Bringing Food To The Disabled
    Building A House For Habitat For Humanity
    Building Dollhouses
    Bus spotting
    Butterfly Watching
    Button Collecting
    Cake Decorating
    Calligraphy
    Camping
    Candle making
    Canoeing
    Car Racing
    Card collecting
    Cartooning
    Casino Gambling
    Cave Diving
    Ceramics
    Cheerleading
    Chess
    Church/church activities
    Cigar Smoking
    Climbing
    Cloud Watching
    Coin Collecting
    Collecting
    Collecting Antiques
    Collecting Artwork
    Collecting Hats
    Collecting Music Albums
    Collecting RPM Records
    Collecting Sports Cards (Baseball, Football, Basketball, Hockey)
    Collecting Swords
    Color guard
    Coloring
    Comic book collecting
    Compose Music
    Computer activities
    Computer programming
    Conworlding
    Cooking
    Cosplay
    Cosplaying
    Couponing
    Crafts
    Crafts (unspecified)
    Creative writing
    Cricket
    Crochet
    Crocheting
    Cross-Stitch
    Crossword Puzzles
    Cryptography
    Curling
    Cycling
    Dance
    Dancing
    Darts
    Debate
    Deltiology (postcard collecting)
    Diecast Collectibles
    Digital arts
    Digital Photography
    Disc golf
    Do it yourself
    Dodgeball
    Dog sport
    Dolls
    Dominoes
    Dowsing
    Drama
    Drawing
    Driving
    Dumpster Diving
    Eating out
    Educational Courses
    Electronics
    Element collecting
    Embroidery
    Entertaining
    Equestrianism
    Exercise (aerobics, weights)
    Exhibition drill
    Exploring new technologies 
    Falconry
    Fast cars
    Felting
    Fencing
    Field hockey
    Figure skating
    Fire Poi
    Fishing
    Fishkeeping
    Flag Football
    Floorball
    Floral Arrangements
    Flower arranging
    Flower collecting and pressing
    Fly Tying
    Flying
    Footbag
    Football
    Foraging
    Foreign language learning
    Fossil hunting
    Four Wheeling
    Freshwater Aquariums
    Frisbee Golf – Frolf
    Gambling
    Games
    Gaming (tabletop games and role-playing games)
    Garage Saleing
    Gardening
    Genealogy
    Geocaching
    Ghost hunting
    Glassblowing
    Glowsticking
    Gnoming
    Go
    Go Kart Racing
    Going to movies
    Golf
    Golfing
    Gongoozling
    Graffiti
    Grip Strength
    Guitar
    Gun Collecting
    Gunsmithing
    Gymnastics
    Gyotaku
    Handball
    Handwriting Analysis
    Hang gliding
    Herping
    Hiking
    Home Brewing
    Home Repair
    Home Theater
    Homebrewing
    Hooping
    Horse riding
    Hot air ballooning
    Hula Hooping
    Hunting
    Ice hockey
    Ice skating
    Iceskating
    Illusion
    Impersonations
    Inline skating
    Insect collecting
    Internet
    Inventing
    Jet Engines
    Jewelry Making
    Jigsaw Puzzles
    Jogging
    Judo
    Juggling
    Jukskei
    Jump Roping
    Kabaddi
    Kart racing
    Kayaking
    Keep A Journal
    Kitchen Chemistry
    Kite Boarding
    Kite flying
    Kites
    Kitesurfing
    Knapping
    Knife making
    Knife throwing
    Knitting
    Knotting
    Lacemaking
    Lacrosse
    Lapidary
    LARPing
    Laser tag
    Lasers
    Lawn Darts
    Learn to Play Poker
    Learning A Foreign Language
    Learning An Instrument
    Learning To Pilot A Plane
    Leather crafting
    Leathercrafting
    Lego building
    Legos
    Letterboxing
    Listening to music
    Locksport
    Machining
    Macramé
    Macrame
    Magic
    Mahjong
    Making Model Cars
    Marbles
    Marksmanship
    Martial arts
    Matchstick Modeling
    Meditation
    Metal detecting
    Meteorology
    Microscopy
    Mineral collecting
    Model aircraft
    Model building
    Model Railroading
    Model Rockets
    Modeling Ships
    Models
    Motor sports
    Motorcycles
    Mountain Biking
    Mountain Climbing
    Mountaineering
    Movie and movie memorabilia collecting
    Mushroom hunting/Mycology
    Musical Instruments
    Nail Art
    Needlepoint
    Netball
    Nordic skating
    Orienteering
    Origami
    Owning An Antique Car
    Paintball
    Painting
    Papermache
    Papermaking
    Parachuting
    Paragliding or Power Paragliding
    Parkour
    People Watching
    Photography
    Piano
    Pigeon racing
    Pinochle
    Pipe Smoking
    Planking
    Playing music
    Playing musical instruments
    Playing team sports
    Poker
    Pole Dancing
    Polo
    Pottery
    Powerboking
    Protesting
    Puppetry
    Puzzles
    Pyrotechnics
    Quilting
    R/C Boats
    R/C Cars
    R/C Helicopters
    R/C Planes
    Racing Pigeons
    Racquetball
    Radio-controlled car racing
    Rafting
    Railfans
    Rappelling
    Rapping
    Reading
    Reading chronicles of freedom fighters
    Reading To The Elderly
    Record collecting
    Relaxing
    Renaissance Faire
    Renting movies
    Rescuing Abused Or Abandoned Animals
    Robotics
    Rock balancing
    Rock climbing
    Rock Collecting
    Rockets
    Rocking AIDS Babies
    Roleplaying
    Roller derby
    Roller skating
    Rugby
    Rugby league football
    Running
    Sailing
    Saltwater Aquariums
    Sand art
    Sand Castles
    Scrapbooking
    Scuba diving
    Sculling or Rowing
    Sculpting
    Sea glass collecting
    Seashell collecting
    Self Defense
    Sewing
    Shark Fishing
    Shooting
    Shooting sport
    Shopping
    Shortwave listening
    Singing
    Singing In Choir
    Skateboarding
    Skating
    Skeet Shooting
    Sketching
    Skiing
    Skimboarding
    Sky Diving
    Skydiving
    Slack Lining
    Slacklining
    Sleeping
    Slingshots
    Slot car racing
    Snorkeling
    Snowboarding
    Soap Making
    Soapmaking
    Soccer
    Socializing with friends/neighbors
    Speed Cubing (rubix cube)
    Speed skating
    Spelunkering
    Spending time with family/kids
    Sports
    Squash
    Stamp Collecting
    Stand-up comedy
    Stone collecting
    Stone skipping
    Storm Chasing
    Storytelling
    String Figures
    Sudoku
    Surf Fishing
    Surfing
    Survival
    Swimming
    Table football
    Table tennis
    Taekwondo
    Tai chi
    Tatting
    Taxidermy
    Tea Tasting
    Tennis
    Tesla Coils
    Tetris
    Textiles
    Texting
    Tombstone Rubbing
    Tool Collecting
    Tour skating
    Toy Collecting
    Train Collecting
    Train Spotting
    Trainspotting
    Traveling
    Treasure Hunting
    Trekkie
    Triathlon
    Tutoring Children
    TV watching
    Ultimate Frisbee
    Urban exploration
    Vehicle restoration
    Video game collecting
    Video Games
    Video gaming
    Videophilia
    Vintage cars
    Violin
    Volleyball
    Volunteer
    Walking
    Warhammer
    Watching movies
    Watching sporting events
    Water sports
    Weather Watcher
    Web surfing
    Weightlifting
    Windsurfing
    Wine Making
    Wingsuit Flying
    Wood carving
    Woodworking
    Working In A Food Pantry
    Working on cars
    World Record Breaking
    Worldbuilding
    Wrestling
    Writing
    Writing Music
    Writing Songs
    Yo-yoing
    Yoga
    YoYo
    Ziplining
    Zumba"""



    nlp_text=nlp(resume_text)

    tokens = [token.text for token in nlp_text if not token.is_stop]
    result={}
    
    for j,i in enumerate(tokens):
      if i.lower()=='hobbies':
        j+=1
        x=tokens[j]
        ans=''
        while j<len(tokens) or x!='\n':
          if (nlp(x)[0].pos_ in ['NOUN','VERB'] or x.lower() in temp.lower()):
            ans=ans+x+''
            if x=='\n':
              break
            if j<len(tokens) and nlp(tokens[j+1])[0].pos_ == 'SPACE':
              j+=1
            if x=='\n':
              break
            if (nlp(x)[0].pos_=='NOUN' or nlp(x)[0].pos_=='VERB') and j<len(tokens) and nlp(tokens[j+1])[0].pos_ not in ['NOUN','SPACE','PUNCT']:
              ans=ans+', '
          j+=1
          if j>=len(tokens) or x=='\n':
            break
          x=tokens[j]
        ans=ans.replace(' ,',',')
        result[0]=ans
        break
    return result

  def extract_location(self, text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    gpe = [] # countries, cities, states
    for ent in doc.ents:
      if (ent.label_ == 'GPE'):
          gpe.append(ent.text)
      if gpe == None:
        return print("No location is mentioned in resume")
    return gpe

  def extract_phone_number(self, resume_text):
    '''Accepts text as string and returns the first occurence of a phone number
    '''
    try:
      return re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'), resume_text).group().strip()
    except:
      return ""

  def extract_email(self, doc):
    email = re.findall("[\w.+-]+@[\w-]+\.[\w.-]+", doc)
    return email

  def extract_name(self,resume_text):
      matcher=Matcher(nlp.vocab)  
      nlp_text = nlp(resume_text)
      
      # First name and Last name are always Proper Nouns
      pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
      
      matcher.add('NAME', [pattern])
      
      matches = matcher(nlp_text)
      
      for match_id, start, end in matches:
          span = nlp_text[start:end]
          return span.text
  matcher1=Matcher(nlp.vocab)
  def extract_linkedin(self, resume_text):
    linkedin = re.findall(r'linkedin.com/i?n?/?[\w\.-]+', resume_text)
    return linkedin
  def extract_github(self, resume_text):
    github = re.findall(r'github.com/i?n?/?[\w\.-]+', resume_text)
    return github