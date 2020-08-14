import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime # Used to record time of transaction

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# The above configuration was provided by CS50 - Following is my work

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation")
        # Ensure password and confirmation match up
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("passsword and confirmation do not match")

        # Generate hash for password
        hash = generate_password_hash(request.form.get("password"))
        # Query the USERS table to inert a new user
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash);",
                                username=request.form.get("username"),
                                hash=hash)

        # Ensure the user was registered
        if not new_user_id:
            return apology("username is taken")

        # Start a new session for the user
        session["user_id"] = new_user_id

        # Go to homepage
        return redirect("/")

    # User reached route via GET (as by requesting the page via GET)
    else:
        # Return the rendered page
        return render_template("register.html")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Query API for data
        API_data = lookup(request.form.get("symbol"))
        # Ensure API has given data
        if API_data == None:
            return apology("incorrect symbol")

        # Return HTML page with API data
        return render_template("quoted.html", name=API_data["name"], price=usd(API_data["price"]), symbol=API_data["symbol"])

    else:
        return render_template("quote.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("incorrect symbol")
        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("provide number of shares")

        # Assign shares to a variable
        shares = int(request.form.get("shares"))

        # Ensure shares is a positive number
        if shares <= 0:
            return apology("provide positive number of shares")

        # Assign symbol to a variable
        symbol = request.form.get("symbol")

        # Query API for data
        API_data = lookup(symbol)

        # Ensure API has given data
        if API_data == None:
            return apology("no such symbol")

        # Calculate total of buying shares
        price_per_share = API_data["price"]
        total_buy = price_per_share * shares

        # Query the USERS table to know user's funds
        USERS_data = db.execute("SELECT * FROM users WHERE id = :id;", id=session["user_id"])

        # USERS_data is a list of dictionaries
        funds = USERS_data[0]["cash"]

        if funds < total_buy:
            return apology("not enough money")
        else:
            funds -= total_buy

        # Update the USERS table with reduced cash amount
        db.execute("UPDATE users SET cash = :funds WHERE id = :user_id;",
                    funds=funds,
                    user_id=session["user_id"])

        # Insert a new transaction field into the TRANSACTIONS table
        db.execute("INSERT INTO transactions (symbol, shares, price, date, person_id) " \
                    "VALUES (:symbol, :shares, :price, :date, :person_id);",
                    symbol=symbol, shares=shares,
                    price=usd(API_data["price"]), date=datetime.now(),
                    person_id=session["user_id"])

        # Ensure that the user has not previously bought this type of share
        PORTFOLIO_data = db.execute("SELECT symbol, shares FROM portfolio " \
                        "WHERE symbol = :symbol AND person_id = :person_id;",
                        symbol=symbol,
                        person_id = session["user_id"])

        # Ensure that the user has no shares of this symbol in the PORTFOLIO table
        if len(PORTFOLIO_data) == 0:
            db.execute("INSERT INTO portfolio (symbol, name, shares, person_id) " \
                        "VALUES (:symbol, :name, :shares, :person_id);",
                        symbol=symbol, name=API_data["name"],
                        shares=shares, person_id=session["user_id"])
        # If the user has this type of share, just update the number of shares in the PORTFOLIO table
        else:
            shares += PORTFOLIO_data[0]["shares"]
            db.execute("UPDATE portfolio SET shares = :shares WHERE symbol = :symbol;",
                        shares=shares,
                        symbol=symbol)

        # Go to homepage
        return redirect("/")

    # User reached route via GET (as by requesting the page via GET)
    else:
        return render_template("buy.html")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Retrieve user information
    user_info = db.execute("SELECT symbol, name, shares FROM portfolio WHERE person_id = :id;",
                            id=session["user_id"])

    # Dictionary for storing current prices on owned shares
    current_share_prices = {}
    current_share_prices_multiplied = {}

    # Variable to know how much funds stored in shares
    overall_shares_fund = 0

    # Iterate through user data to determine prices on user's shares
    for row in user_info:
        API_data = lookup(row["symbol"])
        # Fill in the dictionary with current prices
        current_share_prices[row["symbol"]] = usd(API_data["price"])
        current_share_prices_multiplied[row["symbol"]] = usd(API_data["price"] * row["shares"])

        # Add to total fund of owned shares
        overall_shares_fund += (API_data["price"] * row["shares"])

    # Query the USERS table for the funds remaining
    funds_left = db.execute("SELECT cash FROM users WHERE id = :id;",
                            id = session["user_id"])[0]["cash"]

    # Variable to hold total value of portfolio
    total_funds = overall_shares_fund + funds_left

    # Return HTML page with retreived data (looping and displaying is in index.html)
    return render_template("index.html", user_info=user_info,
                            current_share_prices=current_share_prices,
                            current_share_prices_multiplied=current_share_prices_multiplied,
                            funds_left=usd(funds_left),
                            total_funds=usd(total_funds))

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("incorrect symbol")
        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("provide number of shares")

        # Assign shares to a variable and have it positive
        shares = abs(int(request.form.get("shares")))

        # Ensure shares is not zero
        if shares == 0:
            return apology("you cannot sell zero shares")

        # Assign symbol to a variable
        symbol = request.form.get("symbol")

        # Query the API for the current price
        API_data = lookup(symbol)

        # Ensure provided symbol is legitimate
        if API_data == None:
            return apology("incorrect symbol")

        # Query the PORTFOLIO table for the number of owned shares of this symbol
        PORTFOLIO_data = db.execute("SELECT shares FROM portfolio WHERE person_id = :id AND symbol = :symbol;",
                                    id=session["user_id"],
                                    symbol=symbol)

        # Ensure that user has this type of shares
        if len(PORTFOLIO_data) == 0:
            return apology("you do not own such symbol shares")

        # Ensure the user has enough shares to sell
        if PORTFOLIO_data[0]["shares"] < shares:
            return apology("not enough shares")

        # Calculate the total price for shares being sold
        total_to_sell = API_data["price"] * shares

        # Query the USERS table for funds available
        USERS_data = db.execute("SELECT * FROM users WHERE id = :id;",
                                id=session["user_id"])
        user_funds = USERS_data[0]["cash"]

        # Add sold shares price to user funds
        user_funds += total_to_sell

        # Update the USERS table with increased funds
        db.execute("UPDATE users SET cash = :cash WHERE id = :id;",
                    cash=user_funds,
                    id=session["user_id"])

        # Convert shares to negative
        # (for it to be recorded with minus in the TRANSACTIONS table)
        shares = shares * -1

        # Insert a new transaction record into the TRANSACTIONS table
        db.execute("INSERT INTO transactions (symbol, shares, price, date, person_id) " \
                    "VALUES (:symbol, :shares, :price, :date, :person_id);",
                    symbol=symbol, shares=shares, price=usd(API_data["price"]),
                    date=datetime.now(), person_id=session["user_id"])

        # Calculate how much shares left in the PORTFOLIO table
        # += is because shares was converted to negative (see above)
        shares += PORTFOLIO_data[0]["shares"]

        # Update the PORTFOLIO table with the reduced number of shares
        db.execute("UPDATE portfolio SET shares = :shares WHERE person_id = :id AND symbol = :symbol;",
                    shares=shares, id=session["user_id"],
                    symbol=symbol)

        # Check if the user has no more shares of that symbol
        PORTFOLIO_data = db.execute("SELECT shares FROM portfolio " \
                                    "WHERE person_id = :id AND symbol = :symbol;",
                                    id=session["user_id"],
                                    symbol=symbol)

        # If the PORTFOLIO table has 0 shares for the symbol, DELETE the record
        if PORTFOLIO_data[0]["shares"] == 0:
            db.execute("DELETE FROM portfolio WHERE person_id = :id AND symbol = :symbol",
                        id=session["user_id"], symbol=symbol)
        return redirect("/")

    else:
        return render_template("sell.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Retrieve information from the TRANSACTIONS table
    TRANSACTIONS_data = db.execute("SELECT symbol, shares, price, date FROM transactions WHERE person_id = :id;",
                            id=session["user_id"])

    # Return HTML page with retreived data (looping and displaying is in index.html)
    return render_template("history.html", TRANSACTIONS_data=TRANSACTIONS_data)

# Personal Touch - Change password
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change password"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure old password was submitted
        if not request.form.get("old"):
            return apology("please submit old password")
        # Ensure new password was submitted
        elif not request.form.get("new"):
            return apology("please submit new password")

        # Retirieve old password hash from the USERS table
        old_hash = db.execute("SELECT hash FROM users WHERE id = :id;",
                            id=session["user_id"])[0]["hash"]

        # Compare hashes
        if not check_password_hash(old_hash, request.form.get("old")):
            return apology("incorrect password")

        # Generate new hash for new password and UPDATE the USERS table
        new_hash = generate_password_hash(request.form.get("new"))
        db.execute("UPDATE users SET hash = :hash WHERE id = :id;",
                    hash=new_hash, id=session["user_id"])

        return redirect("/")

    # User reached route via GET (as by requesting the page via GET)
    else:
        return render_template("password.html")

# The following functions were provided by CS50 - Above is my work

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
