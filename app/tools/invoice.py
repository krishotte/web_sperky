from fpdf import Template
from pathlib import Path

item_label_1 = {
    'name': 'item_label_1', 'type': 'T',
    'x1': 25.0, 'y1': 145, 'x2': 100.0, 'y2': 152,
    'multiline': False, 'font': 'Roboto',
    'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0,
    'foreground': 0, 'background': 0,
    'align': 'I', 'text': 'Názov a popis položky', 'priority': 2,
}
item_label_2 = {
    'name': 'item_label_2', 'type': 'T',
    'x1': 100.0, 'y1': 145, 'x2': 120.0, 'y2': 152,
    'multiline': True, 'font': 'Roboto',
    'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0,
    'foreground': 0, 'background': 0,
    'align': 'I', 'text': 'Počet', 'priority': 2,
}

item_label_3 = {
    'name': 'item_label_3', 'type': 'T',
    'x1': 120.0, 'y1': 145, 'x2': 160.0, 'y2': 152,
    'multiline': True, 'font': 'Roboto',
    'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0,
    'foreground': 0, 'background': 0,
    'align': 'I', 'text': 'Jednotková cena', 'priority': 2,
}

item_label_4 = {
    'name': 'item_label_4', 'type': 'T',
    'x1': 160.0, 'y1': 145, 'x2': 185.0, 'y2': 152,
    'multiline': True, 'font': 'Roboto',
    'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0,
    'foreground': 0, 'background': 0,
    'align': 'I', 'text': 'Celkom', 'priority': 2,
}


def create(order, products, filename):
    elements = [
        # left column - supplier
        {
            'name': 'dodavatel_heading', 'type': 'T',
            'x1': 25.0, 'y1': 35.0, 'x2': 100.0, 'y2': 43.0,
            'multiline': False, 'font': 'RobotoB',
            'size': 12, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': '', 'priority': 3, },
        {
            'name': 'dodavatel', 'type': 'T',
            'x1': 25.0, 'y1': 43, 'x2': 100.0, 'y2': 49,
            'multiline': True, 'font': 'Roboto',
            'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': '', 'priority': 2,
        },
        {
            'name': 'ico', 'type': 'T',
            'x1': 25.0, 'y1': 76, 'x2': 100.0, 'y2': 81,
            'multiline': True, 'font': 'Roboto',
            'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': '', 'priority': 2,
        },

        {
            'name': 'payment', 'type': 'T',
            'x1': 25.0, 'y1': 102, 'x2': 100.0, 'y2': 108,
            'multiline': True, 'font': 'Roboto',
            'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': '', 'priority': 2,
        },

        # right column - receiver
        {
            'name': 'invoice', 'type': 'T',
            'x1': 105.0, 'y1': 28.0, 'x2': 185.0, 'y2': 36.0,
            'multiline': False, 'font': 'Roboto',
            'size': 18.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': '', 'priority': 2,
        },
        {
            'name': 'order', 'type': 'T',
            'x1': 105.0, 'y1': 36.0, 'x2': 185.0, 'y2': 43.0,
            'multiline': False, 'font': 'Roboto',
            'size': 14.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': '', 'priority': 2,
        },
        {
            'name': 'odberatel_heading', 'type': 'T',
            'x1': 105.0, 'y1': 50.0, 'x2': 185.0, 'y2': 56.0,
            'multiline': False, 'font': 'RobotoB',
            'size': 12, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0x111111, 'background': 0x111111,
            'align': 'I', 'text': '', 'priority': 3, },
        {
            'name': 'odberatel', 'type': 'T',
            'x1': 105.0, 'y1': 58, 'x2': 185.0, 'y2': 64,
            'multiline': True, 'font': 'Roboto',
            'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': '', 'priority': 2,
        },
        {
            'name': 'odberatel_address_heading', 'type': 'T',
            'x1': 105.0, 'y1': 90.0, 'x2': 185.0, 'y2': 98.0,
            'multiline': False, 'font': 'RobotoB',
            'size': 12, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0x111111, 'background': 0x111111,
            'align': 'I', 'text': '', 'priority': 3, },
        {
            'name': 'odberatel_address', 'type': 'T',
            'x1': 105.0, 'y1': 98, 'x2': 185.0, 'y2': 104,
            'multiline': True, 'font': 'Roboto',
            'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': '', 'priority': 2,
        },

        {
            'name': 'terminy_label', 'type': 'T',
            'x1': 105.0, 'y1': 124, 'x2': 150.0, 'y2': 130,
            'multiline': True, 'font': 'Roboto',
            'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': '', 'priority': 2,
        },
        {
            'name': 'terminy_values', 'type': 'T',
            'x1': 155.0, 'y1': 124, 'x2': 185.0, 'y2': 130,
            'multiline': True, 'font': 'Roboto',
            'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': '', 'priority': 2,
        },

        # lines
        {
            'name': 'vline1', 'type': 'L',
            'x1': 100.0, 'y1': 28.0, 'x2': 100.0, 'y2': 140.0,
            'size': 0.2, 'priority': 2, 'text': '',
            'foreground': 0x888888,
        },
        {
            'name': 'hline1', 'type': 'L',
            'x1': 20.0, 'y1': 95.0, 'x2': 100.0, 'y2': 95.0,
            'size': 0.2, 'priority': 2, 'text': '',
            'foreground': 0x888888,
        },
        {
            'name': 'hline2', 'type': 'L',
            'x1': 100.0, 'y1': 46.0, 'x2': 190.0, 'y2': 46.0,
            'size': 0.2, 'priority': 2, 'text': '',
            'foreground': 0x888888,
        },
        {
            'name': 'hline3', 'type': 'L',
            'x1': 100.0, 'y1': 120.0, 'x2': 190.0, 'y2': 120.0,
            'size': 0.2, 'priority': 2, 'text': '',
            'foreground': 0x888888,
        },
        {
            'name': 'hline4', 'type': 'L',
            'x1': 20.0, 'y1': 140.0, 'x2': 190.0, 'y2': 140.0,
            'size': 0.2, 'priority': 2, 'text': '',
            'foreground': 0x888888,
        },
        item_label_1, item_label_2, item_label_3, item_label_4,
        {
            'name': 'hline5', 'type': 'L',
            'x1': 20.0, 'y1': 154.0, 'x2': 190.0, 'y2': 154.0,
            'size': 0.2, 'priority': 2, 'text': '',
            'foreground': 0x888888,
        },
    ]

    # ordered products section
    offset = 156
    for index, product in enumerate(products):
        # offset = 155 + index * 10
        name = {
            'name': f'p_{product["id"]}', 'type': 'T',
            'x1': 25.0, 'y1': offset, 'x2': 100.0, 'y2': offset + 7,
            'multiline': True, 'font': 'Roboto',
            'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': product["name"], 'priority': 2,
        }
        if 'variants' in product:
            variant = {
                'name': f'v_{product["id"]}', 'type': 'T',
                'x1': 25.0, 'y1': offset + 6, 'x2': 100.0, 'y2': offset + 6 + 7,
                'multiline': True, 'font': 'Roboto',
                'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0,
                'foreground': 0, 'background': 0,
                'align': 'I', 'text': product["variants"][0]["name"], 'priority': 2,
            }

        count = {
            'name': f'c_{product["id"]}', 'type': 'T',
            'x1': 100.0, 'y1': offset, 'x2': 120.0, 'y2': offset + 7,
            'multiline': True, 'font': 'Roboto',
            'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': str(product["pivot"]["product_count"]), 'priority': 2,
        }
        unit_price = {
            'name': f'up_{product["id"]}', 'type': 'T',
            'x1': 120.0, 'y1': offset, 'x2': 160.0, 'y2': offset + 7,
            'multiline': True, 'font': 'Roboto',
            'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': str(product["pivot"]["unit_price"]) + ' EUR', 'priority': 2,
        }
        complete_price = {
            'name': f'cp_{product["id"]}', 'type': 'T',
            'x1': 160.0, 'y1': offset, 'x2': 180.0, 'y2': offset + 7,
            'multiline': True, 'font': 'Roboto',
            'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': str(product["pivot"]["unit_price"] * product["pivot"]["product_count"])  + ' EUR', 'priority': 2,
        }
        elements.append(name)
        elements.append(count)
        elements.append(unit_price)
        elements.append(complete_price)
        if 'variants' in product:
            elements.append(variant)
            offset += 6
        offset += 8

        hline = {
            'name': f'hline_{product["id"]}', 'type': 'L',
            'x1': 20.0, 'y1': offset, 'x2': 190.0, 'y2': offset,
            'size': 0.2, 'priority': 2, 'text': '',
            'foreground': 0x888888,
        }
        elements.append(hline)
        offset += 2

    shipping_label = {
            'name': f'ship_label', 'type': 'T',
            'x1': 25.0, 'y1': offset, 'x2': 120.0, 'y2': offset + 7,
            'multiline': False, 'font': 'Roboto',
            'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0,
            'foreground': 0, 'background': 0,
            'align': 'I', 'text': f'Spôsob dopravy: {order["shipping"]["name"]}', 'priority': 2,
        }
    shipping_price = {
        'name': f'ship_price', 'type': 'T',
        'x1': 160.0, 'y1': offset, 'x2': 185.0, 'y2': offset + 7,
        'multiline': False, 'font': 'Roboto',
        'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0,
        'foreground': 0, 'background': 0,
        'align': 'I', 'text': f'{order["shipping"]["price"]} EUR', 'priority': 2,
    }
    offset +=8
    hline6 = {
        'name': 'hline6', 'type': 'L',
        'x1': 20.0, 'y1': offset, 'x2': 190.0, 'y2': offset,
        'size': 0.2, 'priority': 2, 'text': '',
        'foreground': 0x888888,
    }
    offset += 2
    elements.append(shipping_label)
    elements.append(shipping_price)
    elements.append(hline6)

    dph = {
        'name': 'dph', 'type': 'T',
        'x1': 25.0, 'y1': offset + 4, 'x2': 120.0, 'y2': offset + 10,
        'multiline': False, 'font': 'Roboto',
        'size': 10, 'bold': 0, 'italic': 0, 'underline': 0,
        'foreground': 0, 'background': 0,
        'align': 'I', 'text': 'Poznámka: Nie sme platiteľmi DPH', 'priority': 3, }
    total_price_label = {
        'name': 'tpl', 'type': 'T',
        'x1': 120.0, 'y1': offset + 4, 'x2': 160.0, 'y2': offset + 10,
        'multiline': False, 'font': 'RobotoB',
        'size': 12, 'bold': 0, 'italic': 0, 'underline': 0,
        'foreground': 0, 'background': 0,
        'align': 'I', 'text': 'Celková cena: ', 'priority': 3, }
    total_price = {
        'name': 'tp', 'type': 'T',
        'x1': 160.0, 'y1': offset + 4, 'x2': 185.0, 'y2': offset + 10,
        'multiline': False, 'font': 'RobotoB',
        'size': 12, 'bold': 0, 'italic': 0, 'underline': 0,
        'foreground': 0, 'background': 0,
        'align': 'I', 'text': f'{order["total_price"]} EUR', 'priority': 3, }
    elements.append(total_price_label)
    elements.append(total_price)
    elements.append(dph)

    # here we instantiate the template and define the HEADER
    f = Template(format="A4", elements=elements,
                 title=f'Faktúra {order["invoice"]["prefix"]}{order["invoice"]["year"]}{str(order["invoice"]["number"]).zfill(4)}')
    f.pdf.add_font('Roboto', '', 'storage/static/fonts/Roboto-Regular.ttf', uni=True)
    f.pdf.add_font('RobotoB', '', 'storage/static/fonts/Roboto-Bold.ttf', uni=True)
    f.pdf.set_font('Roboto', '', 14)

    f.add_page()

    # we FILL some of the fields of the template with the information we want
    # note we access the elements treating the template instance as a "dict"
    f["dodavatel_heading"] = "DODÁVATEĽ:"


    f["dodavatel"] = "Viera Fajtáková\nPri cintoríne 1320\n908 73 Veľké Leváre\nSlovensko"
    f["ico"] = "IČO: 41101898\nDIČ: 1073329774"

    ib = "IBAN: SK38 0900 0000 0051 3467 9672"
    vs = "xxxxxxxxx"
    payment_form = "Bankovým prevodom"
    f["payment"] = f'{ib}\nVariabilný symbol: {order["invoice"]["variable_symbol"]}\nKonštantný symbol: 0008\nForma úhrady: {payment_form}\n'

    number = "20210001"
    f["invoice"] = f'Faktúra č.: {order["invoice"]["prefix"]}{order["invoice"]["year"]}{str(order["invoice"]["number"]).zfill(4)}'
    f["order"] = f'Objednávka č.: {order["name"]}'

    f["odberatel_heading"] = "ODBERATEĽ:"
    f["odberatel"] = f"{order['address']['name']}\n{order['address']['street']}\n{order['address']['zip_code']} {order['address']['city']}"

    f["odberatel_address_heading"] = "DODACIA ADRESA:"
    f["odberatel_address"] = f"{order['address']['name']}\n{order['address']['street']}\n{order['address']['zip_code']} {order['address']['city']}"

    f["terminy_label"] = "Dátum vystavenia:\nDátum splatnosti"

    f["terminy_values"] = f'{order["invoice"]["issue_date"]}\n{order["invoice"]["due_date"]}'

    # and now we render the page

    f.render(str(filename))
