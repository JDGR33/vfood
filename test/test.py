import vfood.main as fs

fs.scrape_prep_data(
    [
        "tomate",
        "ggg",
        "cerveza",
        "pan",
        "huevos",
        "carne",
        "pollo",
        "harina pan",
        "harina de trigo",
        "jabon",
        "chocolate",
        "queso",
        "pavo",
        "salchica",
    ]
).to_excel("test_5.xlsx")
