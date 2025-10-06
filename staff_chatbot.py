import json
import re
from fuzzywuzzy import fuzz
import nltk
import spacy

#NLTK stuff
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize stemmer
stemmer = nltk.PorterStemmer()

#Spacy is loaded
try:
    nlp = spacy.load("en_core_web_sm")
    print(" spaCy NLP loaded.")
except:
    nlp = None
    print(" spaCy model not found. NLP features limited.")

#Staff chat bot is defined
class StaffChatbot:
    def __init__(self):
        try:
            with open('knowledge_base.json', 'r') as f:
                self.knowledge_base = json.load(f)
            print(" Knowledge base loaded with", len(self.knowledge_base), "entries.")
        except Exception as e:
            print(" Failed to load knowledge base:", e)
            self.knowledge_base = []

        #Mangae the dialogues 
        self.awaiting_location = False
        self.awaiting_blockage_type = False
        self.last_entry_candidates = []
        self.last_intent = None

     #Fuzzy used
    def fuzzy_match_location(self, user_input):
        best_score = 0
        best_match = None
        for entry in self.knowledge_base:
            score = fuzz.partial_ratio(user_input.lower(), entry['location'].lower())
            if score > best_score and score >= 80:
                best_score = score
                best_match = entry['location'].lower()
        return best_match
    
    #Location extratio is doen using mutiple method 
    def extract_location(self, user_input):
        user_input_lower = user_input.lower()
        #Mathc the codes
        for entry in self.knowledge_base:
            if entry['code'].lower() in user_input_lower:
                return [entry]
        matched = []
        #Match the location
        for entry in self.knowledge_base:
            if entry['location'].lower() in user_input_lower:
                matched.append(entry)
        if matched:
            return matched
        #recognzation using Spacy
        if nlp:
            doc = nlp(user_input)
            entities = [ent.text.lower() for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
            noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
            for entry in self.knowledge_base:
                if any(loc in entry['location'].lower() for loc in entities + noun_chunks):
                    matched.append(entry)
            if matched:
                return matched
             #Fallback if incase
        fuzzy_loc = self.fuzzy_match_location(user_input)
        if fuzzy_loc:
            matched = [entry for entry in self.knowledge_base if entry['location'].lower() == fuzzy_loc]
            if matched:
                return matched
        return []
    
    #Dtermine the user inten
    def detect_intent(self, text: str) -> str:
        text_lower = text.lower()
        end_keywords = ['thank you', 'thanks', 'bye', 'no more help', 'that’s all', 'i’m done', 'exit']
        if any(k in text_lower for k in end_keywords):
            return "end"

        blockage_keywords = {
            'block', 'blockage', 'issue', 'problem', 'disruption',
            'delay', 'cancel', 'cancelled', 'engineering', 'incident'
        }

        #stemming and lemmatization
        tokens = re.findall(r'\b\w+\b', text_lower)
        stemmed_tokens = {stemmer.stem(word) for word in tokens}
        lemmatized_tokens = {token.lemma_ for token in nlp(text_lower)} if nlp else set()
        all_normalized = stemmed_tokens.union(lemmatized_tokens)

         #blockage keywords used for intent detection
        for kw in blockage_keywords:
            if stemmer.stem(kw) in all_normalized or kw in all_normalized:
                return "blockage_info"
        return "unknown"
    
    #KB information returend
    def answer_kb_query(self, entry):
        response = f" Disruption at **{entry['location']}** ({entry['code']}):\n"
        response += f" Blockage Type: {entry['blockage'].capitalize()}\n"
        response += f" Advice: {entry['advice']}\n"
        response += f" Staff Notes: {entry['staff_notes']}\n"
        response += " Alternative Transport: " + ", ".join(entry['alt_transport']) + "\n"
        response += f" Passenger Info: {entry['passenger_notes']}"
        return response
    
    #This generates responses
    def generate_response(self, user_input):
        if self.awaiting_blockage_type:
            bt = user_input.strip().lower()
            if bt in ["partial", "full"]:
                for entry in self.last_entry_candidates:
                    if entry["blockage"].lower() == bt:
                        self.awaiting_blockage_type = False
                        return self.answer_kb_query(entry)
                return f"No {bt} blockage found for the specified location."
            else:
                return "Please specify if the blockage is **partial** or **full**."
            
        #For location waiting 
        if self.awaiting_location:
            self.awaiting_location = False
            entries = self.extract_location(user_input)
            if not entries:
                return " Sorry, I couldn’t find disruption information for that location."
            elif len(entries) == 1:
                return self.answer_kb_query(entries[0])
            else:
                self.awaiting_blockage_type = True
                self.last_entry_candidates = entries
                return "ℹ There are multiple disruption types. Is the blockage **partial** or **full**?"
            
         #Intent detection
        intent = self.detect_intent(user_input)
        if intent == "end":
            return "You're welcome! If you need further assistance, feel free to ask. Goodbye! "
        
         #Blockage quires handeled this 
        if intent == "blockage_info":
            entries = self.extract_location(user_input)
            if not entries:
                self.awaiting_location = True
                return " Where is the disruption occurring?"
            elif len(entries) == 1:
                return self.answer_kb_query(entries[0])
            else:
                self.awaiting_blockage_type = True
                self.last_entry_candidates = entries
                return "ℹ There are multiple disruption types. Is the blockage **partial** or **full**?"

        return " I’m here to help with train service disruptions. You can tell me about any blockage or issue."

 #Used for direct lauch 
if __name__ == "__main__":
    print(" Staff Chatbot Initialized. Type 'exit' to quit.")
    bot = StaffChatbot()
    while True:
        try:
            msg = input("Staff: ").strip()
            if msg.lower() in ['exit', 'quit']:
                print(" Goodbye!")
                break
            reply = bot.generate_response(msg)
            print("Bot:", reply)
        except KeyboardInterrupt:
            print("\n Exiting...")
            break