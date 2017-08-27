import feedparser
import re

def build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': speech_output
        },
        'card': {
            'type': 'Simple',
            'title': card_title,
            'content': card_output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
     }


def build_response(session_attributes, speechlet_response):
    return {
        'sessionAttributes': session_attributes,
        'response': speechlet_response
     }
     
def arxiv_handler(Paper):
    categories = {u'computer science - operating systems': u'cs.os', u'statistics - methodology': u'stat.me', u'physics - mesoscopic systems and quantum hall effect': u'cond-mat.mes-hall', u'mathematics - dynamical systems': u'math.ds', u'quantitative biology - quantitative methods': u'q-bio.qm', u'mathematics - algebraic geometry': u'math.ag', u'mathematics - operator algebras': u'math.oa', u'computer science - graphics': u'cs.gr', u'computer science - mathematical software': u'cs.ms', u'computer science - symbolic computation': u'cs.sc', u'quantum physics': u'quant-ph', u'quantitative biology - biomolecules': u'q-bio.bm', u'mathematics - algebraic topology': u'math.at', u'nonlinear sciences - chaotic dynamics': u'nlin.cd', u'mathematics - probability': u'math.pr', u'mathematics - statistics': u'math.st', u'computer science - architecture': u'cs.ar', u'nuclear experiment': u'nucl-ex', u'mathematics - functional analysis': u'math.fa', u'mathematics - logic': u'math.lo', u'physics - data analysis; statistics and probability': u'physics.data-an', u'computer science - learning': u'cs.lg', u'nonlinear sciences - cellular automata and lattice gases': u'nlin.cg', u'physics - physics education': u'physics.ed-ph', u'computer science - digital libraries': u'cs.dl', u'physics - general physics': u'physics.gen-ph', u'mathematics - history and overview': u'math.ho', u'physics - chemical physics': u'physics.chem-ph', u'computer science - general literature': u'cs.gl', u'quantitative biology - molecular networks': u'q-bio.mn', u'computer science - performance': u'cs.pf', u'physics - computational physics': u'physics.comp-ph', u'mathematics - number theory': u'math.nt', u'computer science - multimedia': u'cs.mm', u'quantitative biology - tissues and organs': u'q-bio.to', u'mathematics - numerical analysis': u'math.na', u'mathematics - spectral theory': u'math.sp', u'physics - instrumentation and detectors': u'physics.ins-det', u'physics - atmospheric and oceanic physics': u'physics.ao-ph', u'mathematics - analysis of pdes': u'math.ap', u'physics - atomic and molecular clusters': u'physics.atm-clus', u'computer science - logic in computer science': u'cs.lo', u'statistics - computation': u'stat.co', u'physics - soft condensed matter': u'cond-mat.soft', u'computer science - numerical analysis': u'cs.na', u'quantitative biology - subcellular processes': u'q-bio.sc', u'quantitative biology - populations and evolution': u'q-bio.pe', u'statistics - machine learning': u'stat.ml', u'mathematics - classical analysis and odes': u'math.ca', u'quantitative biology - genomics': u'q-bio.gn', u'general relativity and quantum cosmology': u'gr-qc', u'physics - history of physics': u'physics.hist-ph', u'computer science - networking and internet architecture': u'cs.ni', u'nonlinear sciences - pattern formation and solitons': u'nlin.ps', u'computer science - computational complexity': u'cs.cc', u'computer science - data structures and algorithms': u'cs.ds', u'computer science - computers and society': u'cs.cy', u'physics - plasma physics': u'physics.plasm-ph', u'quantitative biology - other': u'q-bio.ot', u'physics - strongly correlated electrons': u'cond-mat.str-el', u'statistics - theory': u'stat.th', u'computer science - other': u'cs.oh', u'mathematical physics': u'math-ph', u'high energy physics - lattice': u'hep-lat', u'mathematics - commutative algebra': u'math.ac', u'physics - accelerator physics': u'physics.acc-ph', u'mathematics - k-theory and homology': u'math.kt', u'physics - classical physics': u'physics.class-ph', u'mathematics - rings and algebras': u'math.ra', u'mathematics - quantum algebra': u'math.qa', u'computer science - artificial intelligence': u'cs.ai', u'statistics - applications': u'stat.ap', u'high energy physics - theory': u'hep-th', u'physics - atomic physics': u'physics.atom-ph', u'physics - medical physics': u'physics.med-ph', u'mathematics - metric geometry': u'math.mg', u'physics - superconductivity': u'cond-mat.supr-con', u'astrophysics': u'astro-ph', u'mathematics - differential geometry': u'math.dg', u'computer science - programming languages': u'cs.pl', u'physics - other': u'cond-mat.other', u'mathematics - general mathematics': u'math.gm', u'high energy physics - phenomenology': u'hep-ph', u'physics - materials science': u'cond-mat.mtrl-sci', u'physics - statistical mechanics': u'cond-mat.stat-mech', u'quantitative biology - neurons and cognition': u'q-bio.nc', u'computer science - information retrieval': u'cs.ir', u'mathematics - information theory': u'math.it', u'nonlinear sciences - exactly solvable and integrable systems': u'nlin.si', u'physics - geophysics': u'physics.geo-ph', u'computer science - discrete mathematics': u'cs.dm', u'computer science - cryptography and security': u'cs.cr', u'high energy physics - experiment': u'hep-ex', u'computer science - software engineering': u'cs.se', u'computer science - computer vision and pattern recognition': u'cs.cv', u'computer science - robotics': u'cs.ro', u'computer science - information theory': u'cs.it', u'quantitative biology - cell behavior': u'q-bio.cb', u'physics - disordered systems and neural networks': u'cond-mat.dis-nn', u'computer science - computer science and game theory': u'cs.gt', u'computer science - computation and language': u'cs.cl', u'computer science - multiagent systems': u'cs.ma', u'physics - space physics': u'physics.space-ph', u'nonlinear sciences - adaptation and self-organizing systems': u'nlin.ao', u'mathematics - representation theory': u'math.rt', u'mathematics - group theory': u'math.gr', u'physics - popular physics': u'physics.pop-ph', u'mathematics - geometric topology': u'math.gt', u'computer science - computational engineering; finance; and science': u'cs.ce', u'mathematics - general topology': u'math.gn', u'computer science - computational geometry': u'cs.cg', u'mathematics - optimization and control': u'math.oc', u'computer science - databases': u'cs.db', u'physics - biological physics': u'physics.bio-ph', u'mathematics - category theory': u'math.ct', u'computer science - human-computer interaction': u'cs.hc', u'physics - optics': u'physics.optics', u'computer science - neural and evolutionary computing': u'cs.ne', u'mathematics - mathematical physics': u'math.mp', u'computer science - sound': u'cs.sd', u'nuclear theory': u'nucl-th', u'mathematics - symplectic geometry': u'math.sg', u'physics - physics and society': u'physics.soc-ph', u'computer science - distributed; parallel; and cluster computing': u'cs.dc', u'physics - fluid dynamics': u'physics.flu-dyn', u'mathematics - complex variables': u'math.cv', u'mathematics - combinatorics': u'math.co'}
    catString = ""
    for key in categories:
        if Paper.lower().encode("utf8") in key:
            if catString == "":
                catString = catString + categories[key]
            else:
                catString = catString + "+" + categories[key]
    if catString == "":
        Paper = Paper.replace(" ","+")
        api_url = "http://export.arxiv.org/api/query?search_query=all:"+Paper.lower()+"&start=0&max_results=20"
    else:
        api_url = "http://export.arxiv.org/api/query?search_query=cat:"+catString+"&start=0&max_results=20"
    response = feedparser.parse(api_url)

    if (response["entries"] == []):
        Paper = Paper.replace(" ","+")
        api_url = "http://export.arxiv.org/api/query?search_query=all:"+Paper.lower()+"&start=0&max_results=20"
        response = feedparser.parse(api_url)
        
    if response["entries"] == []:
        return "NOT_FOUND"

    data = []
    
    for i in response["entries"]:
        i["title"] = re.sub("\n"," ",i["title"])
        i["summary"] = re.sub("\n"," ",i["summary"])
        i["title"] = re.sub("\$"," dollar sign ",i["title"])
        i["summary"] = re.sub("\$"," dollar sign ",i["summary"])
        i["title"] = re.sub("/"," forward slash  ",i["title"])
        i["summary"] = re.sub("/"," forward slash ",i["summary"])
        
        json = {"title": i["title"] ,
                "summary":i["summary"]}
        data.append(json)
    
    return data

def start_intent(session_attributes, category):
    papers = arxiv_handler(category)
    if papers == "NOT_FOUND":
        card_title = category + " was not found"
        card_output = "Sorry :) "+category+" was not found. Check later if anything has been added"
        speech_output = card_title
        reprompt_text = ""
        should_end_session = True
        return build_response({}, build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session))
    session_attributes["index"] = 0
    session_attributes["state"] = "GO_TO_SUMMARY"
    session_attributes["papers"] = papers
    card_title = session_attributes["papers"][0]["title"]
    speech_output = "Here are the "+str(len(session_attributes["papers"]))+" most recent papers in "+category+". " + card_title + ". Would you like to listen to the summary?"
    reprompt_text = "You can say yes to listen to the summary"
    card_output = session_attributes["papers"][0]["summary"]
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session))

def yes_intent(session_attributes):
    if session_attributes["state"] == "GO_TO_SUMMARY":
        card_title = session_attributes["papers"][session_attributes["index"]]["title"]
        speech_output = session_attributes["papers"][session_attributes["index"]]["summary"] + ". Would you like to go the next paper?"
        card_output = session_attributes["papers"][session_attributes["index"]]["summary"]
        reprompt_text = "Say yes to go to the next paper or no to exit"
        should_end_session = False
        session_attributes["state"] = "GO_TO_TITLE"
        session_attributes["index"] = session_attributes["index"] + 1
        return build_response(session_attributes, build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session))
        
    elif session_attributes["state"] == "GO_TO_TITLE":
        session_attributes["state"] = "GO_TO_SUMMARY"
        return summary(session_attributes)
    
def no_intent(session_attributes):
    if session_attributes["state"] == "GO_TO_SUMMARY":
        session_attributes["index"] = session_attributes["index"] + 1
        return summary(session_attributes)
        
    elif session_attributes["state"] == "GO_TO_TITLE":
        return exit()

def next_intent(session_attributes):
    session_attributes["index"] = session_attributes["index"] + 1
    if session_attributes["state"] == "GO_TO_TITLE":
        session_attributes["state"] = "GO_TO_SUMMARY"
    return summary(session_attributes)

def summary(session_attributes):
    card_title = session_attributes["papers"][session_attributes["index"]]["title"]
    speech_output = "Okay. The next paper is " +card_title + ". Would you like to listen to the summary?"
    reprompt_text = "You can say yes to listen to this summary"
    card_output = session_attributes["papers"][session_attributes["index"]]["summary"]
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session))
    
def exit():
    card_title = "Thank You"
    card_output = "Check later for more papers :)"
    speech_output = "Thank you for Pre Print Archive. Check later for more papers"
    reprompt_text = ""
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session))

def error():
    card_title = "Invalid Option"
    card_output = "It seems like you've used an invalid option. Try again"
    speech_output = "It seems like you've used an invalid option. Why don't you try again?"
    reprompt_text = "You can ask Pre Print Archive for recent papers in electrons, for starters"
    should_end_session = False
    return build_response({}, build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session))

def help():
    card_title = "Help"
    card_output = "To start, you can ask Pre Print Archive for recent papers in machine learning :)"
    speech_output = """Pre Print Archive is a skill that allows you to listen through the 20 most recent papers in your preferred category.
                        To start, you can say get recent papers in combinatorics or whatever category you want.
                        You can say yes to listen to a brief summary or no go to the next paper.
                        You can always skip the summary by saying next. So what kind of papers do you wanna listen to today?"""
    reprompt_text = ""
    should_end_session = False
    return build_response({}, build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session))

def main(event, context=None):
    if(event["request"]["type"] == "IntentRequest"):
        intent_name = event["request"]["intent"]["name"]
        if(intent_name=="StartIntent"):
            if "value" in event["request"]["intent"]["slots"]["category"]:
                category = event["request"]["intent"]["slots"]["category"]["value"]
                event["session"]["attributes"] = {}
                return start_intent(event["session"]["attributes"] ,category)
            else:
                return error()
        elif (intent_name=="AMAZON.StopIntent" or intent_name == "AMAZON.CancelIntent"):
            return exit()
        elif (intent_name=="AMAZON.HelpIntent"):
            return help()
        elif "attributes" in event["session"]:
            if event["session"]["attributes"] != {}:
                if (event["session"]["attributes"]["index"] < len(event["session"]["attributes"]["papers"])-1):
                    if (intent_name=="YesIntent"):
                        return yes_intent(event["session"]["attributes"])
                    elif (intent_name=="NoIntent"):
                        return no_intent(event["session"]["attributes"])
                    elif (intent_name=="NextIntent"):
                        return next_intent(event["session"]["attributes"])
                else:
                    return exit()
            else:
                return error()
        else:
            return error()

    if(event["request"]["type"] == "LaunchRequest"):
        card_title = "Welcome to ArXiv for Alexa"
        card_output = "To start, ask pre print arXiv for recent papers in machine learning"
        speech_output = "Welcome to Archive for Alexa. To start ask pre print archive for recent papers in machine learning"
        reprompt_text = "You can also ask for recent papers in any other category"
        should_end_session = False
        return build_response({}, build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session))
