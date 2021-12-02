from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Bid, Watchlist, Category, Status

active_status_id = 1

def index(request):
    try:
        active_status = Status.objects.get(pk= active_status_id)
        listings = active_status.listings.all()
    except:
        listings = None

    return render(request, "auctions/index.html", {
        'listings': listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    categories = Category.objects.all()

    if request.method == "POST":
        if request.user.is_authenticated:
            title = request.POST.get('title')
            description = request.POST.get('description')
            bid_amount = request.POST.get('bid')
            url = request.POST.get('image_url')
            lister = request.user
            category_name = request.POST.get("category")
            category = Category.objects.filter(name=category_name).first()

            url_id = "".join(str(title).split())

            bid = Bid.objects.create(amount=bid_amount)
            bid.save

            listing = Listing.objects.create(title=title, description=description, bid=bid, url=url, lister=lister, category=category)
            listing.save()

            return HttpResponseRedirect(reverse('listing', args=(listing.pk, )))
        else:
            return render(request, "auctions/register.html")

    return render(request, "auctions/create_listing.html", { "categories": categories })

def listing(request, listing_id):
    # required title, description, current bid, image url, and comments info
    item = Listing.objects.get(pk=listing_id)
    bid = getattr(item, 'bid')
    user = request.user

    try:
        watchlist = Watchlist.objects.get(user=user)
    except Watchlist.DoesNotExist:
        watchlist = Watchlist.objects.create(user=user)
        watchlist.save()

    comments = Comment.objects.all()

    #updating bid value
    if request.method == "POST":
        new_bid = int(request.POST.get('bid'))

        if new_bid > bid.amount:
            bid.amount = new_bid
            bid.bidder = request.user

            bid.save()

            return render(request, "auctions/listing.html", {
                'listing': item,
                'bid': bid,
                'comments': comments,
                'id': listing_id,
                'watchlist': watchlist.listing.all(),
            })

        return render(request, "auctions/listing.html", {
        'listing': item,
        'bid': bid,
        'comments': comments,
        'id': listing_id,
        'watchlist': watchlist.listing.all(),
        'message': "You can't place a bid with amount less than or equal to current bid."
        })
    #end

    return render(request, "auctions/listing.html", {
        'listing': item,
        'bid': bid,
        'comments': comments,
        'id': listing_id,
        'watchlist': watchlist.listing.all(),
    })

def comment(request, listing_id):
    comment = request.POST.get('comment')
    user = request.user
    listing = Listing.objects.get(pk= listing_id)


    comment_object = Comment.objects.create(comment=comment, commenter=user)
    comment_object.save()

    return HttpResponseRedirect(reverse('listing', args=(listing_id, )))

def watchlist(request):
    try:
        watchlist = Watchlist.objects.get(user=request.user)
        watchlist_items = watchlist.listing.all()
    except:
        watchlist_items = None

    return render(request, "auctions/watchlist.html", { 
        "watchlist": watchlist_items,
    })

def watchlist_add(request, listing_id):
    item = Listing.objects.get(pk= listing_id)
    user = request.user

    try:
        watchlist = Watchlist.objects.get(user=user)
    except Watchlist.DoesNotExist:
        watchlist = Watchlist.objects.create(user=user)
        watchlist.save()

    watchlist.listing.add(item)

    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))



def watchlist_remove(request, listing_id):
    item = Listing.objects.get(pk= listing_id)
    user = request.user
    watchlist = Watchlist.objects.get(user=user)

    watchlist.listing.remove(item)

    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def categories(request):
    categories_list = Category.objects.all()

    return render(request, "auctions/categories.html", { 'categories': categories_list, })

def get_category(request, category_id):
    category = Category.objects.get(pk= category_id)
    listings = category.category_items.all()

    return render(request, 'auctions/get_category.html', { 'listings': listings, 'category': category})

def close_listing(request, listing_id):
    listing = Listing.objects.get(pk= listing_id)

    listing.status = Status.objects.get(pk= 2)
    listing.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))