import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
from dotenv import load_dotenv
import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

load_dotenv()

auth_token = os.getenv("AUTH_TOKEN")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

anthropic = Anthropic()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# Global dictionary to hold chat histories
chat_histories = {}

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = update.message.text

    # Initialize history list if not present for the chat_id
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []

    # Add the new message to the history
    chat_histories[chat_id].append(message)

    # Format the history for the prompt
    formatted_history = "\n".join(f"{HUMAN_PROMPT} {msg}" for msg in chat_histories[chat_id])
    
    # Build the prompt for Claude with the history
    prompt = f"{formatted_history}\n{AI_PROMPT}"

    # Call Claude's API with the prompt
    completion = anthropic.completions.create(
        model="claude-2.0",
        max_tokens_to_sample=150,
        temperature=1,
        prompt=prompt,
    )
    
    # Assuming the completion has an attribute called 'completion' that holds the result
    response_text = completion.completion

    # Add Claude's response to the history as well
    chat_histories[chat_id].append(response_text)

    # Send Claude's response to the Telegram chat
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    completion = anthropic.completions.create(
        model="claude-2.0",
        max_tokens_to_sample=150,
        temperature=1,
        prompt=f"${HUMAN_PROMPT} Human: You will be acting as a highly skilled French teacher named Joe. Your goal is to summarise news articles at the student's language level (A1) to teach them new vocabulary and give them reading practice.\nHere are some important rules for the interaction:\n- Your summaries should never be more than 4 sentences long and each sentence should be on a new line. \n- Your sentences should be as short as possible.\n- Your summaries should always introduce between 2 and 6 words\n- You will provide a vocab glossary before the summary with new words and their translation\nHere is an example of how to do a glossary and summary from an article:\n\n<example>\n<article> Volodymyr Zelensky conteste que la guerre en Ukraine se trouve dans une \"impasse\"\nDans le cadre d'une visite de la présidente de la Commission européenne samedi à Kiev, le président ukrainien a contesté que le conflit de son pays avec la Russie se trouve dans une \"impasse\", et déploré que la guerre au Proche-Orient détourne l'attention du monde.\n\nVolodymyr Zelensky accueille Ursula von der Leyen, la présidente de la Commission européenne, à Kiev, pour la sixième fois depuis le début du conflit avec la Russie, le 4 novembre 2023. © Présidence ukrainienne via AFP\n\nMalgré les déclarations pessimistes d'un haut gradé ukrainien, le président Volodymyr Zelensky n'en démord pas : la guerre contre la Russie n'est pas dans une \"impasse\". C'est ce qu'il a déclaré samedi 4 novembre au cours d'une conférence de presse à Kiev avec la présidente de la Commission européenne Ursula von der Leyen, venue discuter du chemin d'adhésion de l'Ukraine à l'UE.\n\n\"Le temps a passé aujourd'hui et les gens sont fatigués (...). Mais nous ne sommes pas dans une impasse\", a affirmé Volodymyr Zelensky, alors qu'un commandant de haut rang a affirmé cette semaine que les deux armées se trouvaient prises au piège d'une guerre d'usure et de positions.\n\nL'Ukraine mène depuis juin une lente contre-offensive pour tenter de libérer les territoires occupés de l'Est et du Sud. Mais, jusqu'ici, les avancées ont été très limitées. La ligne de front, longue de plus de 1 000 km, n'a guère bougé depuis près d'un an et la libération de la ville de Kherson en novembre 2022.\n\nÀ lire aussi**\"Impasse\" tactique, pessimisme occidental... Kiev en quête d'un second souffle face à la Russie**\n\nLe Kremlin avait aussi assuré jeudi que le conflit en Ukraine ne se trouvait pas dans une \"impasse\", contestant des propos du commandant en chef de l'armée ukrainienne, Valery Zaloujny, dans un entretien à The Economist.\n\n\"Tout comme lors de la Première Guerre mondiale, nous avons atteint un niveau technologique tel que nous nous trouvons dans une impasse\", avait déclaré Valery Zaloujny à l'hebdomadaire britannique. \"Il n'y aura probablement pas de percée magnifique et profonde\", avait-il ajouté.\n\n\"Nous allons relever ce défi\"\nLe président Volodymyr Zelensky a démenti toute pression des pays occidentaux pour entamer des négociations avec la Russie. Il a admis que le conflit entre Israël et le mouvement islamiste palestinien Hamas avait \"détourné l'attention\" de la guerre opposant l'Ukraine à la Russie.\n\n\"Nous nous sommes déjà retrouvés dans des situations très difficiles lorsqu'il n'y avait presque aucune focalisation sur l'Ukraine\", a noté le président ukrainien, ajoutant : \"Je suis absolument certain que nous allons relever ce défi.\"\n\nLes soutiens de l'Ukraine, en particulier les États-Unis, répètent qu'ils procureront de l'aide militaire et financière à Kiev jusqu'à la défaite de la Russie.\n\nLors de cette sixième visite d'Ursula von der Leyen en Ukraine depuis le début de l'invasion russe en février 2022, la dirigeante compte aborder le \"soutien militaire\" des Européens, ainsi que \"le douzième paquet de sanctions\" de l'UE contre la Russie, en cours de préparation, a-t-elle déclaré à des journalistes.\"\n </article>\n\n<glossary>\nimpasse: dead end\netre d'accord: agree with\nun conflit: a conflict\nune defaite: a defeat\nplutot que: rather than\n</glossary>\n\n<summary> \nUn general ukrainien a dit que la guerre est a une impasse. \nZelensky n'est pas d'accord.\nZelensky est triste que les gens regardent le conflit entre Israël et la Palestine plutôt que la guerre en Ukraine.\nLes soutiens de l'Ukraine en Occident disent qu'ils aideront Kiev jusqu'à la défaite de la Russie.\n</summary>\n</example>\n\n</example>\n\n<example>\n<article> Au Népal, un séisme de magnitude 5,6 fait plus d'une centaine de morts\nSelon un nouveau bilan provisoire communiqué samedi par les autorités népalaises, au moins 132 personnes sont mortes et plus de 100 ont été blessées dans un tremblement de terre qui a secoué une région reculée du Népal, où les secours s'organisent à la recherche des survivants.\n\nPublié le : 04/11/2023 - 07:30\n\n3 mn\nCette photo fournie par le bureau du Premier ministre népalais montre une zone touchée par le tremblement de terre dans le nord-ouest du Népal, le 4 novembre 2023.\nCette photo fournie par le bureau du Premier ministre népalais montre une zone touchée par le tremblement de terre dans le nord-ouest du Népal, le 4 novembre 2023. © AP\nPar :\nFRANCE 24\nSuivre\nSéisme meurtrier au Népal. Au moins 132 personnes sont mortes dans un tremblement de terre qui a secoué une région reculée du pays, selon un nouveau bilan provisoire communiqué samedi 4 novembre par les autorités népalaises. Sur place, les secours s'organisent à la recherche des survivants.\n\nLe séisme de magnitude 5,6 a été mesuré à une profondeur de 18 km selon l'Institut américain d'études géologiques USGS. Il a frappé l'extrême ouest du pays himalayen tard vendredi soir. Son épicentre a été localisé à 42 km au sud de Jumla, non loin de la frontière avec le Tibet.\n\n\"92 personnes sont mortes à Jajarkot et 40 à Rukum\", a déclaré à l'AFP le porte-parole du ministère de l'Intérieur, Narayan Prasad Bhattarai, citant les deux districts à ce stade les plus touchés par le séisme, situés au sud de l'épicentre dans la province frontalière de Karnali.\n\nPlus de 100 blessés ont été dénombrés dans ces deux districts, a pour sa part affirmé le porte-parole de la police népalaise, Kuber Kathayat.\n\n\"Certaines routes sont bloquées à cause des dégâts\"\nLes forces de sécurité népalaises ont été largement déployées dans les zones touchées par le séisme pour participer aux opérations de secours, selon le porte-parole de la police de la province de Karnali, Gopal Chandra Bhattarai.\n\n\"L'isolement des districts rend difficile la transmission des informations\", a-t-il ajouté. \"Certaines routes sont bloquées à cause des dégâts, mais nous essayons d'atteindre la zone par d'autres voies.\"\n\nÀ Jajarkot, l'hôpital de secteur a été pris d'assaut par les habitants y transportant des blessés.\n\nDes vidéos et des photos publiées sur les réseaux sociaux montrent des habitants fouillant les décombres dans l'obscurité pour extraire des survivants des constructions effondrées. On y voit des maisons en terre détruites ou endommagées et des survivants à l'extérieur pour se protéger de possibles autres effondrements, tandis qu'hurlent les sirènes des véhicules d'urgence.\n\nLe Premier ministre népalais, Pushpa Kamal Dahal, est arrivé samedi dans la zone touchée après avoir exprimé \"sa profonde tristesse pour les dommages humains et physiques causés par le tremblement de terre\".\n\nLe Népal sur une faille géologique majeure\nDes secousses modérées ont été ressenties jusqu'à New Delhi, la capitale de l'Inde située à près de 500 km de l'épicentre.\n\nLe Premier ministre indien Narendra Modi s'est dit \"profondément attristé\" par les pertes humaines au Népal. \"L'Inde est solidaire du peuple népalais et est prête à lui apporter toute l'aide possible\", a-t-il ajouté.\n\nDeeply saddened by loss of lives and damage due to the earthquake in Nepal. India stands in solidarity with the people of Nepal and is ready to extend all possible assistance. Our thoughts are with the bereaved families and we wish the injured a quick recovery. @cmprachanda\n\n— Narendra Modi (@narendramodi) November 4, 2023\nLe résumé de la semaine\nFrance 24 vous propose de revenir sur les actualités qui ont marqué la semaine\n\nJe m'abonne\nLes séismes sont fréquents au Népal, qui se trouve sur une faille géologique majeure où la plaque tectonique indienne s'enfonce dans la plaque eurasienne, formant la chaîne de l'Himalaya. La secousse a été suivie plusieurs heures après par des répliques de magnitude 4 dans le même secteur, selon l'USGS.\n\nPrès de 9 000 personnes sont mortes en 2015 lorsqu'un tremblement de terre de magnitude 7,8 a frappé le Népal, détruisant plus d'un demi-million d'habitations et 8 000 écoles.\n\nDes centaines de monuments et de palais royaux – dont des sites de la vallée de Katmandou, classée au patrimoine mondial de l'Unesco et attirant des touristes de toute la planète – avaient subi des dégâts irréversibles, donnant un grand coup au tourisme népalais.\n\nEn novembre 2022, un séisme de magnitude 5,6 avait fait six morts dans le district de Doti, près du district de Jajarkot frappé vendredi soir.\n </article>\n\n<glossary>\n\ntremblement de terre: earthquake\n\nun blessé: an injured person\n\nla zone touchée: affected area\n\ndégâts: damage\n\n</glossary> \n\n<summary>\nIl y a eu un tremblement de terre au Népal.\n\nPlus de 100 personnes sont mortes.\n\nPlus de 100 personnes sont blessées.\n\nLes routes sont bloquées dans la zone touchée.\n\nIl y a beaucoup de dégâts.\n\n</summary>\n\n\n</example>\n\nHere is the article to summarise for your student:\n<article>\nRugby : les Bleues s'inclinent face au Canada pour leur dernier match du WXV et terminent à la 5e place\nAprès leur défaite face à l'Australie la semaine passée, les Bleues se sont de nouveau inclinées samedi face au Canada (20-29), pour leur dernier match du WXV.\n\nArticle rédigé parfranceinfo: sport\nFrance Télévisions - Rédaction Sport\nPublié le 04/11/2023 08:53\nMis à jour le 04/11/2023 09:15\nTemps de lecture : 1 min\nLes Françaises ont été dominées par les Canadiennes, dans leur dernier match du WXV, à Auckland le 4 novembre 2023. (WORLD RUGBY)\nLes Françaises ont été dominées par les Canadiennes, dans leur dernier match du WXV, à Auckland le 4 novembre 2023. (WORLD RUGBY)\nNouveau coup dur pour les Bleues du XV de France. Après s'être inclinées face à l'Australie la semaine dernière, les Françaises ont encaissé un second revers de suite face au Canada, sur le même score (20-29), samedi 4 novembre à Auckland (Nouvelle-Zélande), pour leur dernier match du WXV, nouveau tournoi international. Une défaite décevante alors que les Bleues avaient largement battu les Canadiennes (36-0) lors du match pour la troisième place du Mondial il y a presque un an.\n\n\nUne 5e place décevante\nPourtant bien entrées dans la partie avec un essai de Pauline Bourdon Sansus (14e) et menant à la pause (10-7), les Bleues sont retombées dans leurs travers, faisant preuve d'indiscipline et d'irrégularité. Les Canadiennes, elles, n'ont pas vacillé et ont enchaîné les essais avec Emily Tuttosi (35e) et Krissy Scurfield (43e et 51e).\n\nMalgré un deuxième essai tricolore, inscrit par Marine Ménager (57e), les Françaises ont commis trop de fautes (12 pénalités concédées) et d'approximations pour espérer la victoire. Après la défaite contre l'Australie, la France s'incline ainsi une nouvelle fois dans la compétition. Une défaite inattendue après le succès historique deux semaines plus tôt face à la Nouvelle-Zélande (18-17), championne du monde en titre. Le XV de France termine ainsi à une décevante 5e place la première édition du WXV. L'Angleterre a remporté la compétition avec trois victoires en autant de matches. </article>\nPut your response in <response></response> tags.\nAssistant: <response>${AI_PROMPT}",
    )
    claude_response = completion.completion
    await context.bot.send_message(chat_id=update.effective_chat.id, text=claude_response)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


if __name__ == '__main__':
    application = ApplicationBuilder().token(auth_token).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    response_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), respond)
    caps_handler = CommandHandler('caps', caps)
    news_handler = CommandHandler('news', news)
    inline_caps_handler = InlineQueryHandler(inline_caps)

    application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    application.add_handler(response_handler)
    application.add_handler(caps_handler)
    application.add_handler(news_handler)
    application.add_handler(inline_caps_handler)

    application.run_polling()

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
