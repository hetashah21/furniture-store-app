from flask import render_template, request, redirect, url_for, flash, session

from shop import app, db, photos
from shop.products.models import Addproduct

def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False 

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Addproduct.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method=="POST":
            DictItems = {product_id: {'name': product.name, 'price': product.price, 'discount': product.discount,
                        'quantity': quantity, 'image': product.image}}
            if 'ShoppingCart' in session:
                print(session['ShoppingCart'])
                if product_id in session['ShoppingCart']:
                    pass
                else:
                    session['ShoppingCart'] = MergeDicts(session['ShoppingCart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['ShoppingCart'] = DictItems
                return redirect(request.referrer)
        else:
            return f'{product_id} {quantity} {request.method}'
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def getCart():
    if 'ShoppingCart' not in session:
        return redirect(request.referrer)
    subtotal = 0
    grandtotal = 0
    for key, product in session['ShoppingCart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price'] * int(product['quantity']))
        subtotal -= discount
        tax = ("%.2f" % (.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('products/carts.html', tax=tax, grandtotal=grandtotal)