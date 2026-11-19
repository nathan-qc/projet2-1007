import gradio as gr
import os, pandas

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

tiermates_html = ""

with open(os.path.join("donnees", "dataset.csv"), "r", encoding="utf-8") as f:
    dataset = pandas.read_csv(f)

def predict_button_clicked(id, type_1, type_2, hp, attack, defense, special_attack, special_defense, speed, coverage, power, status):
    type_1 = types[type_1]
    type_2 = types[type_2]

    tier = "ou" # Put the model function here

    return tier.upper()

types = {
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

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            id = gr.Number(label="Numéro de Pokédex", step=1)
            with gr.Row():
                type_1 = gr.Dropdown(choices=[typename for typename in types if typename != "Aucun"], label="Premier type", interactive=True)
                type_2 = gr.Dropdown(choices=types, label="Deuxième type", interactive=True)
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
            output = gr.Textbox(label="Tier Smogon", interactive=False)
            predict_button = gr.Button("Prédire tier Smogon")
            predict_button.click(fn=predict_button_clicked, outputs=output, api_name="predict_tier", inputs=[
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
            @gr.render(inputs=output)
            def show_tiermates(tier):
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

demo.launch(theme="base")