from flask import render_template
from app import db
from app.models import Submission, Offer
from datetime import datetime,timedelta
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    query = db.session.query(Offer.symbol.distinct().label("symbol"))
    symbols = [row.symbol for row in query.all()]
    gcs = []
    for symbol in symbols:
        try:
            bid = db.session.query(Offer).filter_by(symbol=symbol, type="bid").join(Submission).order_by(Submission.created_at.desc()).first()
            ask = db.session.query(Offer).filter_by(symbol=symbol, type="ask").join(Submission).order_by(Submission.created_at.desc()).first()
            price = (bid.price * bid.qty + ask.price * ask.qty)/(bid.qty + ask.qty)
            #vol = Offer.query.filter_by(symbol=symbol).count()
            vol =  db.session.query(Offer).filter_by(symbol=symbol).join(Submission).filter(Submission.created_at.between(datetime.utcnow() - timedelta(hours=24), datetime.utcnow())).count()
            gc = {"symbol": symbol, "bid": bid.price, "ask": ask.price, "volume": vol, "price": price}
            gcs.append(gc)
        except:
            pass

    return render_template('index.html', title='Home', gcs = gcs)

@bp.route('/<symbol>')
def gc(symbol):
    symbol = symbol.upper()
    #bid = db.session.query(Offer).filter_by(symbol=symbol, type="bid").join(Submission).order_by(Submission.created_at.desc()).first()
    recentBids = db.session.query(Offer).filter_by(symbol=symbol, type="bid").join(Submission).order_by(Submission.created_at.desc()).limit(10).all()
    recentAsks = db.session.query(Offer).filter_by(symbol=symbol, type="ask").join(Submission).order_by(Submission.created_at.desc()).limit(10).all()
    #ask = db.session.query(Offer).filter_by(symbol=symbol, type="ask").join(Submission).order_by(Submission.created_at.desc()).first()
    latestBid = recentBids[0]
    latestAsk = recentAsks[0]
    price = (latestBid.price * latestBid.qty + latestAsk.price * latestAsk.qty)/(latestBid.qty + latestAsk.qty)
    #vol = Offer.query.filter_by(symbol=symbol).count()
    vol = db.session.query(Offer).filter_by(symbol=symbol).join(Submission).filter(Submission.created_at.between(datetime.utcnow() - timedelta(hours=24), datetime.utcnow())).count()

    return render_template('gc.html', gc = gc, bid = latestBid, ask = latestAsk, symbol = symbol, vol = vol, price = price, bids = recentBids, asks=recentAsks, title=symbol)

@bp.route('/about')
def about():
    return render_template('about.html', title='About')

@bp.route('/legal')
def legal():
    return render_template('legal.html', title='Legal')
