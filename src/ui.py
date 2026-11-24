import gradio as gr
import os, pandas, matplotlib
from engine import Engine

TYPES = {
        "Aucun": "none",
        "Normal": "normal", 
        "Feu": "fire",
        "Eau": "water",
        "Plante": "grass",
        "Électrik": "electric",
        "Glace": "ice", 
        "Combat": "fighting",
        "Poison": "poison",
        "Sol": "ground",
        "Vol": "flying",
        "Psy": "psychic",
        "Insecte": "bug",
        "Roche": "rock",
        "Spectre": "ghost",
        "Dragon": "dragon",
        "Ténèbres": "dark",
        "Acier": "steel",
        "Fée": "fairy"
}

def error_popup(message:str)->None:
    """Affiche un message d'erreur
    """
    gr.Warning(message)

def predict_button_clicked(id:int, type_1:str, type_2:str, hp:int, attack:int, defense:int, special_attack:int, special_defense:int, speed:int, coverage:int, power:int, status:int)->tuple[str, matplotlib.figure]:
    """Vérifie les entrées, puis renvoie la prédiction en fonction des variables données
    """
    for input in [id, hp, attack, defense, special_attack, special_defense, speed, coverage, power, status]:
        if not type(input) == type(0):
            error_popup(f"Saise invalide, tous les saisies numériques doivent être des entiers non-négatifs")
            return ""
       
    type_1 = TYPES[type_1]
    type_2 = TYPES[type_2]

    e = Engine("two")

    tier, confidence, fig = e.confidences(id, type_1, type_2,  hp, attack, defense, special_attack, special_defense, speed, coverage, power, status)



    return f"{tier.upper()} ({confidence*100:.2f}%)", fig

def launch_ui()->None:
    """Lance le UI du logiciel
    """
    # Adapté à partir de l'exemple fourni dans https://www.w3schools.com/css/css_grid.asp
    STYLE = '''
    <style>
        .pokecontainer {
        display: grid;
        grid-template-columns: auto auto auto;
        padding: 10px;
        }
        .pokecontainer div {
        display: flex;
        justify-content: center;
        padding: 10px;
        text-align: center;
        font-style: italic;
        }
        .subtitle {
        text-align: center;
        padding: 10px;
        font-weight: bold;
        }
    </style>
    '''

    with open(os.path.join("donnees", "dataset.csv"), "r", encoding="utf-8") as f:
        dataset = pandas.read_csv(f)

    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                id = gr.Number(label="Numéro de Pokédex", step=1)
                with gr.Row():
                    type_1 = gr.Dropdown(choices=[typename for typename in TYPES if typename != "Aucun"], label="Premier type", interactive=True)
                    type_2 = gr.Dropdown(choices=TYPES, label="Deuxième type", interactive=True)
                with gr.Column():
                    coverage = gr.Slider(label="Nombre de types d'attaque uniques", minimum=0, maximum=18, step=1)
                    power = gr.Slider(label="Puissance d'attaque la plus élevée", minimum=0, maximum=250, step=1)
                    status = gr.Number(label="Nombre d'attaques de statut connues")
            with gr.Column():
                hp = gr.Slider(label="PV", step=1, maximum=255)
                attack = gr.Slider(label="Attaque", step=1, maximum=255)
                defense = gr.Slider(label="Défense", step=1, maximum=255)
                special_attack = gr.Slider(label="Attaque spéciale", step=1, maximum=255)
                special_defense = gr.Slider(label="Defense spéciale", step=1, maximum=255)
                speed = gr.Slider(label="Vitesse", step=1, maximum=255)
            with gr.Column():
                predict_button = gr.Button("Prédire tier Smogon")
                tier_box = gr.Textbox(label="Tier Smogon", interactive=False)
                @gr.render(inputs=tier_box)
                def show_tiermates(tier_confidence):
                    tier = tier_confidence.split(" ")[0]
                    if tier != "":
                        tiermates_dataframe = dataset[dataset["tier"] == tier.lower()].sample(n=3)
                        id_1, id_2, id_3 = [id for id in tiermates_dataframe["id"]]
                        name_1, name_2, name_3 = [name.replace("-", " ").title() for name in tiermates_dataframe["name"]]
                    
                        # Adapté à partir de l'exemple fourni dans https://www.w3schools.com/css/css_grid.asp
                        tiermates_html = f'''
                        <html>
                            {STYLE}
                            <div class="subtitle">Voici quelques exemples de Pokémon dans SV {tier}</div>
                            <div class="pokecontainer">
                                <div><img src="https://raw.githubusercontent.com/PokeAPI/sprites/refs/heads/master/sprites/pokemon/{id_1}.png" width="100" height="100"></div>
                                <div><img src="https://raw.githubusercontent.com/PokeAPI/sprites/refs/heads/master/sprites/pokemon/{id_2}.png" width="100" height="100"></div>
                                <div><img src="https://raw.githubusercontent.com/PokeAPI/sprites/refs/heads/master/sprites/pokemon/{id_3}.png" width="100" height="100"></div>
                                <div>{name_1}</div>
                                <div>{name_2}</div>
                                <div>{name_3}</div>
                            </div>
                        </html>
                        '''
                        gr.HTML(tiermates_html)
                figure = gr.Plot()
                predict_button.click(fn=predict_button_clicked, outputs=[tier_box, figure], api_name="predict_tier", inputs=[
                                    id,
                                    type_1,
                                    type_2,
                                    hp,
                                    attack,
                                    defense,
                                    special_attack,
                                    special_defense,
                                    speed,
                                    coverage,
                                    power,
                                    status
                                ])

    demo.launch(theme="base")