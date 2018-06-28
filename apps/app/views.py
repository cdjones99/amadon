from __future__ import unicode_literals
from django.shortcuts import render, redirect

from .models import User, Item, Cart, Order

from django.contrib import messages
import bcrypt


def index(request):
	return render(request, "app/index.html")


def register(request):
	if request.method == "POST":
		User.objects.register(request)
		return redirect("/")
	else:
		return redirect("/")


def login(request):
	try:
		user = User.objects.get(email=request.POST["email"])

		isValid = bcrypt.checkpw(
			request.POST["password"].encode(), user.password.encode())

		print(isValid)

		if isValid:
			print("PASSWORDS MATCH")
			request.session['name'] = user.name
			request.session['email'] = user.email
			request.session['user_id'] = user.id
			return redirect("/home")
		else:
			print("NO MATCH")
			messages.add_message(request, messages.ERROR,
								 "Invalid Credentials!")
			return redirect("/")
	except:
		messages.add_message(request, messages.ERROR,
							 "No user with this email was found!")
		return redirect("/")

def logout(request):
	del request.session["name"]
	del request.session["email"]
	del request.session["user_id"]
	return redirect("/")


def home(request):
	if "user_id" not in request.session:
		return redirect("/")

	item = Item.objects.all()
	print "I'M HERE"
	print "item", len(item)

	context = {
		"item": item,
	}
	return render(request, "app/home.html", context)


def item(request):
	return render(request, "app/item.html")


def addItem(request):
	isValid = Item.objects.createItem(request)
	if isValid:
		return redirect("/home")
	else:
		return redirect("/item")

def editItem(request):
	pass
	#edit_item = Item.objects.get(id=)


def addOrder(request, id):
	user = User.objects.get(id=request.session["user_id"])

	Order.objects.create(
		item = Item.objects.get(id=id),
		cart = Cart.objects.get(user=user),
		quantity = 1
	)
	return redirect("/home")

def renderCart(request):
	print "Render"
	user = User.objects.get(id=request.session["user_id"])
	order = Cart.objects.get(user=user)
	cart = Order.objects.filter(cart=order)
	context = {
		"cart":cart
	}
	return render(request, "app/cart.html", context)

def delete(request, id):
	Order.objects.get(id=id).delete()
	return redirect("/renderCart")


def purchase(request):
	user = User.objects.get(id=request.session["user_id"])

	cart = Cart.objects.get(user=user)
	orders= Order.objects.filter(cart=cart)

	for o in orders:
		o.item.stock=o.item.stock - o.quantity
		o.item.save()

	return render(request,"app/checkout.html")

def update(request):
	pass


def clear_cart(request):
	user = User.objects.get(id=request.session["user_id"])

	cart = Cart.objects.get(user=user)
	Order.objects.filter(cart=cart).delete()

	return redirect("/home") 

#def 