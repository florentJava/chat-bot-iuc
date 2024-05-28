import telebot
from telebot.types import InlineKeyboardButton
import pandas as pd

apikey = '6706312698:AAHi-uNpXItRewisgst3-U-JB1PME9qMdfk'
bot = telebot.TeleBot(apikey)

#les ecoles
df_ecole = pd.read_csv('formationecole.csv')
data_dict_ecole = df_ecole.to_dict('list')

# Assuming data_dict is your dictionary
ecoles_formations = {k: [i for i in v if pd.notna(i)] for k, v in data_dict_ecole.items()}
ecoles_abreviations = ecoles_formations.keys()

cycles = ecoles_formations.keys()
ecoles_noms = ["Institut superieur de technologie et de design industriel",
            "Institut de commerce et d'ingenieurrie d'affaires",
            "Institut d'ingenieurie informatique d'afrique centrale",
            "Programmes internationnaux des sciencs et \n technologies de l'innovation",
            "shool of engineering and applied sciences"]

ecoles_keyboard = telebot.types.InlineKeyboardMarkup()
ecoles_keyboard.row(
telebot.types.InlineKeyboardButton('<< Menu principale', callback_data='menu_principale'))

for cycle , nom in  zip(ecoles_abreviations,ecoles_noms):
    ecoles_keyboard.row(telebot.types.InlineKeyboardButton(nom+" (  "+cycle+" ) ", callback_data=cycle))
    
#les cycles de formation ,  formations et menu de formations

df = pd.read_csv('cycle_formations.csv')

data_dict = df.to_dict('list')



# Assuming data_dict is your dictionary
formations = {k: [i for i in v if pd.notna(i)] for k, v in data_dict.items()}

cycles = formations.keys()

formation_keyboard = telebot.types.InlineKeyboardMarkup()
formation_keyboard.row(
telebot.types.InlineKeyboardButton('<< Menu principale', callback_data='menu_principale'))

for cycle in cycles:
    formation_keyboard.row(telebot.types.InlineKeyboardButton(cycle, callback_data=cycle))
    



#Menu principale de naigation 
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(
    telebot.types.InlineKeyboardButton('1-Nos Formations', callback_data='formations'),
    telebot.types.InlineKeyboardButton('2-Nos Ecoles', callback_data='ecoles')

)
keyboard.row(
    telebot.types.InlineKeyboardButton('3-Nos campus', callback_data='campus'),
    telebot.types.InlineKeyboardButton('4-Constituer son dossier', callback_data='candidatures'),
)   

keyboard.row(
    telebot.types.InlineKeyboardButton('5-Nous contacter', callback_data='autres'),
    telebot.types.InlineKeyboardButton('6-Nos partenaires', callback_data='partenaires'),
) 


#message de bienvenue
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, 
                "Bien venue sur le bot de l'institut universitaire de la cote! \n\n"+
                "Qu'elle renseignement desirez-vous avoir ?""",
                reply_markup=keyboard)


#gestion des evenements de menu
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    
    if call.data == "formations":
        formation_message(call.message)
        
    if call.data == "menu_principale":
        menu_principale(call.message)
    if call.data=="ecoles":
        ecoles_message(call.message)
        
    #evenement des formations
    if call.data in formations:
        formation = formations[call.data]
    
        str_formation = "Les formations  en "+ call.data+" disposnibles sont les suivantes : \n\n"
        for f in formation:
            if f == 'INDUSTRIEL' or f=="COMMERCE ET GESTION" or f=="SANTE" :
                str_formation +='\n--->' +f"_{f}_" + "\n\n"
            else:
                str_formation +='-' +f + "\n"
        bot.send_message(call.message.chat.id,str_formation, reply_markup=formation_keyboard,parse_mode='Markdown')
    #evenement des ecoles
    if call.data in ecoles_abreviations:
        ecole = ecoles_formations[call.data]
    
        str_ecole = "Les formations offertes par "+ call.data+" sont les suivantes : \n\n"
        for f in ecole:
            str_ecole +='-' +f + "\n"
            
        str_ecole = f"*{str_ecole}*"
        bot.send_message(call.message.chat.id, str_ecole, reply_markup=ecoles_keyboard,parse_mode='Markdown')
    
    #evenement pour constituer le dossier
    if call.data == "candidatures":
        
        element = "Pour les camerounais : \n\n"\
                "-Demande manuscrite adresser au directeur de l'ecole de votre choix\n"\
                "-Photocopie de l'acte de naissance\n" \
                "-photocopie certiiee du BAC/ GCE A/L ou tout autre diplome equivalent\n"\
                "-les bulletins de 2nde en Tle pour les cycles prepas, MBA et d'ingenieurie\n"\
                "-Une enveloppe A4 portant l'adresse du candidat\n"\
                "-02 photos d'identites 4x4\n"\
                "-Les releves de notes de L1, L2, et L3 pour les cycles master\n"\
                "-Un CV detaille du candidat pour les cycles master\n"\
                "-Un recu de versement des frais de concours ou d'etudes de dossiers\n"\
                "-Une inscription en ligne a faire  sur le site www.myiuc.com avant le depot du dossier\n\n\n"\
                "Pour les etranges : \n\n"\
                "-Demande manuscrite adresser au directeur de l'ecole de votre choix\n"\
                "-Photocopie de l'acte de naissance\n" \
                "-photocopie certiiee du BAC/ GCE A/L ou tout autre diplome equivalent\n"\
                "-Une enveloppe A4 portant l'adresse du candidat\n"\
                "-02 photos d'identites 4x4\n"\
                "-Les releves de notes de L1, L2, et L3 pour les cycles master\n"\
                "-Un CV detaille du candidat pour les cycles master\n"\
                "-Un recu de versement des frais de concours ou d'etudes de dossiers\n"\
                
        bot.send_message(call.message.chat.id, 
            element,reply_markup=keyboard)
        
    #Evenement autres
    if call.data == "autres":
        autres = "-Boite Psostale : 3001 Douala-Cameroun, sis Logbessou&Akwa\n"\
            "-Whatsapp : +237 699684612 / 678101616\n"\
            "-Facebook/twiter : iucdouala\n"\
            "-Email : iuc@myiuc.com\n"\
            "-Site web : www.myiuc.com\n"\
            "-Telephone : +237 699684612 / 678101616\n"
        bot.send_message(call.message.chat.id, 
            autres,reply_markup=keyboard)
    
    #Evenement campus
    if call.data == "campus":
        campus = "L'IUC a deux campus a savoir :\n\n"\
            "-Campus A :\n"\
                "             -Loacation : Logbessou, Douala\n"\
                "             -Coordonness : https://maps.app.goo.gl/Ykb8DYAqJXYvzyWR6\n\n"\
            "-Campus A :\n"\
                "             -Loacation : Akwa, Douala\n"\
                "             -Coordonness : https://maps.app.goo.gl/JtKFfJwi1UCxofh8A ." \

        bot.send_message(call.message.chat.id, 
            campus,reply_markup=keyboard)
    
    #Evenement partenaires
    if call.data == "partenaires":
        partenaires = "- Ecole nationales superieur polytechnique de Yaounde 1 : \n"\
                    "- Site web : https://polytechnique.cm/ \n\n"\
                        "- University of buea : \n"\
                    "- Site web : https://www.ubuea.cm/ \n\n"\
                        "- Universite de Dschang : \n"\
                    "- Site web : https://www.univ-dschang.org/ \n\n"\
                        "- Le Groupe Vatel : \n"\
                    "- Site web : https://www.vatel.com/ \n\n"\
                        "- L'ISTEC : \n"\
                    "- Site web : https://istec.fr/ \n\n"\
                    "- L'essec  \n"\
                    " Site web : https://essec-douala.cm/ \n\n"
        bot.send_message(call.message.chat.id, partenaires,reply_markup=keyboard)
        
            
        
@bot.message_handler(commands=['menu'])
def menu_principale(message):  
    bot.send_message(message.chat.id, "Qu'elle renseignement desirez-vous avoir sur l'institut universitaire de la cote  ?", reply_markup=keyboard,parse_mode='Markdown')

#fonction d'erreur
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.send_message(message.chat.id, 
            "Je ne comprends pas votre demande. Veuillez choisir une option dans le menu ci-dessous. Pour faire une suggestion veillez choisir l'option 6 ci-dessous Merci!",
            reply_markup=keyboard)

#Menu des formations
def formation_message(message):

    bot.send_message(message.chat.id, 
                "Voici les cycles de formations que nous proposons : ",
                reply_markup=formation_keyboard)

#Menu des ecoles
def ecoles_message(message):
    bot.send_message(message.chat.id, 
                " - Voici les differentes  ecoles de l'institut universitaire de la cote : ",
                reply_markup=ecoles_keyboard)

        
bot.infinity_polling()


