import gradio as gr
import csv

def predict_button_clicked(id, type_1, type_2, hp, attack, defense, special_attack, special_defense, speed, coverage, power, status):
    type_1 = types[type_1]
    type_2 = types[type_2]

    tier = "Ubers" # Put the model function here

    return tier

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
            output = gr.Textbox(label="Tier Smogon")
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

demo.launch(theme="monochrome")