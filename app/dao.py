def load_categories():
    return [
        {
            'id': 1,
            'name': 'Mobile'
        },
        {
            'id': 2,
            'name': 'Tablet'
        }
    ]


def load_products(kw):
    products = [
        {
            'id': 1,
            'name': 'Iphone 15 Pro',
            'description': "Iphone 15 Pro màu titanium thanh lịch, sang trọng vcl",
            'price': 2400,
            'image': '/static/image/iphone15pro.jpg'
        },
        {
            'id': 2,
            'name': 'Iphone 15 Pro',
            'description': "Iphone 15 Pro màu titanium thanh lịch, sang trọng vcl",
            'price': 2400,
            'image': '/static/image/iphone15pro.jpg'
        },
        {
            'id': 3,
            'name': 'Macbook pro',
            'description': "Macbook pro sang trọng, ngồi code trên con này thì hết sẩy con bà bẩy",
            'price': 3600,
            'image': '/static/image/macbookpro.jpg'
        },
        {
            'id': 4,
            'name': 'Ipad Pro 2021',
            'description': "Ipad Pro 2021 cái này cũng đắt vl, đừng mua",
            'price': 2000,
            'image': '/static/image/ipadpro.jpg'
        },
        {
            'id': 5,
            'name': 'Ipad Pro 2022',
            'description': "Ipad Pro 2022 quá đắt, đừng mua phí tiền",
            'price': 2000,
            'image': '/static/image/ipadpro2.jpg'
        }
    ]
    if kw:
        results = []
        for c in products:
            if c['name'].find(kw) >= 0:
                results.append(c)
        products = results
    return products
