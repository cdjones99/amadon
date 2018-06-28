from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
	def register(self, request):
		if len(request.POST["name"]) < 1:
			messages.add_message(request, messages.ERROR, "Name is required!")
		if len(request.POST["email"]) < 1:
			messages.add_message(request, messages.ERROR, "Email is required!")
		if not EMAIL_REGEX.match(request.POST["email"]):
			messages.add_message(request, messages.ERROR,
								 "Invalid email format! Ex: test@test.com")
		if len(request.POST["password"]) < 8:
			messages.add_message(request, messages.ERROR,
								 "Password must be between 8-32 characters!")
		if request.POST["password"] != request.POST["confirm"]:
			messages.add_message(request, messages.ERROR,
								 "Password and Password Confirmation must match!")
		if User.objects.filter(email=request.POST["email"]).count() > 0:
			messages.add_message(request, messages.ERROR,
								 "A user with this email already exists!")

		if len(get_messages(request)) > 0:
			return False
		else:
			user = User.objects.create(
				name=request.POST["name"],
				email=request.POST["email"],
				password=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
			)
			Cart.objects.create(
				user = user
			)
			return True

	def login(self, request):
		pass


class User(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	objects = UserManager()


class ItemManager(models.Manager):
	def createItem(self, request):
		if len(request.POST["name"]) < 1:
			messages.add_message(request, messages.ERROR, "Name is required!")
		if len(request.POST["price"]) < 1:
			messages.add_message(request, messages.ERROR, "Price is required!")
		if len(request.POST["stock"]) < 1:
			messages.add_message(request, messages.ERROR, "Quantity is required!")
		if len(get_messages(request)) > 0:
			return False
		else:
			Item.objects.create(
				name=request.POST["name"],
				price=request.POST["price"],
				stock=request.POST["stock"],
			)
			return True
		

class Item(models.Model):
	name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=20, decimal_places=2)
	stock = models.IntegerField()
	objects = ItemManager()

class CartManager(models.Manager):
		pass

class Cart(models.Model):
	#items = models.ForeignKey(Item, related_name="user_carts")
	user = models.ForeignKey(User, related_name="cart")
	#user = models.OneToOneField(User, related_name="cart", on_delete=models.PROTECT)

# class OrderManager(models.Manager):
# 	def manage_order(self, request):
# 		if request.POST["date_by"]
# 			messages.add_message(request, messages.ERROR, "Date is required!")
# 		else:
# 			if request.POST["start_date"] < datetime.date.today:
# 				print "Start date must be valid!"
# 				messages.add_message(request, messages.ERROR, "Start date must be valid!")
# 			if request.POST["end_date"] <= request.POST["start_date"]:
# 				messages.add_message(request, messages.ERROR, "End date must be valid!")

class Order(models.Model):
	cart = models.ForeignKey(Cart, related_name="items")
	item = models.ForeignKey(Item, related_name="carts") #on_delete=models.CASCADE
	date_by = models.DateField(blank=True, null=True)
	quantity = models.IntegerField()
	#objects = OrderManager()
