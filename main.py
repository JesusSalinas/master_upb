from src.app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()

# txt = 'Yo te quiero como el mar quiere al río, como la noche quiere al día, como el sol a la luna, como la luz al día.'
# txt_eng = 'I love you like the sea loves the river, like the night loves the day, like the sun loves the moon, like light loves the day.'
# connector = AIOpenAPI()
# response = connector.prompt('Analiza el siguiente texto', txt_eng, 500)
# tx = response.choices[0].text.strip()
# print(tx)