from flask import render_template, request, redirect, url_for, flash, session

from shop import app, db, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets

@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f"The brand '{getbrand}' was added to your database", "success")
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')

@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        flash(f"The category '{getcat}' was added to your database", "success")
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')

@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        desc = form.desc.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, desc=desc, brand_id=brand,
                             category_id=category, image=image)
        db.session.add(addpro)
        flash(f"The product '{name}' has been added to your database", "success")
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title="Add Product page", form=form, brands=brands, categories=categories)