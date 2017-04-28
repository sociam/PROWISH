import json
import re
import csv
import os
from collections import defaultdict

mobtrackers = ['Inmobi', 'Mopub', 'Facebook', 'Chartboost', 'Crashlytics', 'Heyzap', 'Applovin', 'Unitytechnologies', 'Vungle', 'Fyber', 'Millenialmedia', 'Ironsource', 'Tapjoy', 'Flurry', 'Google', 'Bitstadium', 'Presage', 'Comscore', 'Umeng', 'Tencent', 'Nexage', 'Mixpanel', 'Appboy', 'Yandex', 'Kochava', 'Urbanairship', 'Daum', 'Milkman', 'Playhaven', 'Umeng', 'Mail.Ru', 'Newrelic', 'Admob', 'Moat', 'Smaato', 'Admarvel', 'Appodeal', 'Cauley', 'Revmob', 'Adbuddiz', 'Igaworks', 'Nativex', 'Smartadserver', 'Mobfox', 'Pubnative', 'Hyprmx', 'Pingstart', 'Tune', 'Baidu', 'Swrve', 'Tnkfactory', 'Appnext', 'Tencent']
webtrackers = ['Google', 'Doubleclick', 'Facebook', 'Cloudfront', 'Scorecardresearch', 'Appnexus', 'Twitter', 'Amazon', 'Criteo', 'Yahoo', 'Oracle', 'Quantcast', 'Iponweb', 'Adobe', 'Openx', 'Ghostery', 'Rubicon', 'Bluekai', 'Cloudflare', 'Liveramp', 'The Nielsen Company', 'Demdex', 'Truste', 'Newrelic', 'Integral Ad Science', 'Adsrvr', 'Moatads', 'Pubmatic', 'Turn', 'Indexchange', 'Doubleverify', 'Mathtag', 'Chartbeat', 'Optimizely', 'Youtube', 'Tapad', 'Exelate', 'Targus', 'Lotame', 'Sizmek', 'Iasds', 'Neustar', 'Jquery', 'Krxd', 'Adroll', 'Brightroll', 'Audiencescience', 'Bootstrap', 'Rocketfuel', 'Dataxu', 'Tubemogul', 'Microsoft', 'Yandex', 'Conversant', 'Videology', 'Flashtalking', 'Akamai', 'Adap.Tv', 'Magnetic', 'Dstillery', 'Baidu', 'Smartadserver', 'Taboola', 'H&R Block', 'Tealium', 'Convertro', 'MSN', 'Linkedin', 'Mookie1', 'Contextweb', 'Liverail', 'Yadro', 'Bug', 'Chango', 'Conversant Llc', 'Trueffect', 'Signal-Privacy', 'Crazy Egg', 'Drawbridge Inc', 'Sovrn', 'Ovh', 'Exponential', 'Yieldoptimizer', 'Spotxchange', 'Owneriq', 'Insightexpress', 'Adform', 'Automattic', 'Disqus', 'Outbrain', 'Flipps', 'Centromedia', 'Ignitionone', 'Skimlinks', 'Simpli.Fi', 'Wordpress', 'Openx Technologies', 'Ensighten', 'Visual Website Optimizer', 'Rhythmone', 'Mixpanel', 'Sonobi', 'Hotjar', 'Voicefive', 'Gssprt', 'At Internet', 'Ml314', 'Radiumone', 'Parsely', 'Improve Digital Bv', 'Gumgum', 'Amgdgt', 'Effective Measure', 'Pinterest', 'Vk', 'Adition', 'Exoclick', 'Ixi Corporation', 'Nugg.Ad', 'Umeng', 'Alibaba', 'Marketo', 'Gskinner', 'Gigya', 'Tns', 'Eq Works', 'Cxense Asa', 'Steelhouse', 'Yieldlab', '33Across', 'Mail.Ru', 'Pingdom Ab', 'Smart Adserver', 'Brightcove', 'Postrelease', 'Adriver', 'Pagefair', 'Microad', 'Marin Software', 'Collective', 'Trafficjunky', 'Pixalate', 'Demandbase', 'Yieldbot', 'Visualdna', 'Ioam', 'Signal', 'Shopzilla', 'Sharethrough', 'Rambler', 'Clicktale', 'Sociomantic', 'Datonics', 'Run', 'Myspace', 'Taobao', 'Adgear Technologies', 'Sharethis', 'Mybuys', 'Stroeer Media', 'The Mcgraw-Hill Companies', 'Vizury', 'Abc', 'Dyn', 'Longtail Ad Solutions', 'Netseer', 'Smaato', 'The Adex Gmbh', 'Adblade', 'Mxptint', 'Maxymiser', 'Admeta', 'Mcro', 'Sourcepoint Technologies', 'Yieldmanager', 'Rfihub', 'Bounce Exchange', 'Wtp', 'Convertmedia', 'Rackspace Us', 'Eyeview', 'Qualtrics', 'Intent Iq', 'Stickyads.Tv', 'Soasta', 'Cedexis Inc', 'Weborama', 'Invite Media', 'Histats', 'Statcounter', 'Paypal', 'Bidr', 'Springserve', 'Yahoo', 'Nexstar Broadcasting', 'Triplelift', 'Polar', 'Adelphic Inc', 'Deep Forest Media', 'Cedexis', 'Richrelevance', 'Resonate', 'Impact-Ad', 'Jivox', 'Mediade', 'Liveperson', 'Zedo', 'Yabidos', 'Adfox', 'Fout', 'Switch', 'Navegg S.A.', 'Adsnative', 'Eyeota Limited', 'Jsdelivr', 'Consumerinfo.Com', 'Brandscreen Pty Ltd', 'Mythings', 'Polar Mobile Group', 'Answercloud', 'Komoona', 'Admeta', 'Meltdsp', 'Appier Inc', 'Netdna', 'Budgetedbauer', 'Gfk', 'Bidtheatre', 'Research Now', 'Undertone Networks', 'Viglink', 'Adbrain', 'Adstir', 'Sailthru', 'Vimeo', 'Mediametrie', 'Livefyre', 'Mediaforge', 'Webklipper', 'Tencent', 'Ib-Ibi']
trackers = set(mobtrackers)|set(webtrackers)
obj  = json.load(open('company-details.json'))
toptrackers = obj.copy()
for tracker in trackers:
	if toptrackers[tracker]["id"] not in trackers:
		toptrackers.pop(tracker)
for tracker in toptrackers:
	domains = toptrackers[tracker]["domains"]
	fulldomains = filter(None, domains)
	toptrackers[tracker]["domains"] = fulldomains

def getDomainCo(host):
	for tracker in toptrackers:
		for domain in toptrackers[tracker]["domains"]:
			if domain in host:
				return toptrackers[tracker]["id"]

libtoco = {'com.purplebrain.adbuddiz.sdk': 'adbuddiz', 'com.admarvel.android': 'admarvel', 'com.apptracker.android': 'admob', 'com.adobe.flashruntime': 'adobe', 'com.adobe.air': 'adobe', 'com.adobe.adms': 'adobe', 'com.amazon.device.iap': 'amazon', 'com.amazon.ags': 'amazon', 'com.amazon.identity.auth.device': 'amazon', 'com.amazon.insights': 'amazon', 'org.anddev.andengine': 'andengine', 'org.andengine.opengl': 'andengine', 'org.andengine.input': 'andengine', 'org.andengine.entity': 'andengine', 'org.andengine.engine': 'andengine', 'org.andengine.audio': 'andengine', 'org.andengine.util': 'andengine', 'org.andengine.ui': 'andengine', 'org.apache.commons.codec': 'apache', 'com.appboy.models': 'appboy', 'com.appboy.ui': 'appboy', 'com.applovin.impl': 'applovin', 'com.applovin.sdk.air.android': 'applovin', 'com.appnext.ads': 'appnext', 'com.appodeal.ads': 'appodeal', 'com.duapps.ad': 'baidu', 'net.hockeyapp.android': 'bitstadium', 'io.card.payment': 'card.io', 'com.fsn.cauly': 'cauley', 'com.chartboost.sdk': 'chartboost', 'com.comscore.utils': 'comscore', 'com.handmark.pulltorefresh.library': 'core', 'com.crashlytics.android': 'crashlytics', 'net.daum.adam': 'daum', 'io.fabric.sdk.android.services': 'fabric', 'com.facebook.share': 'facebook', 'com.facebook.ads.internal': 'facebook', 'com.facebook.common': 'facebook', 'com.facebook.imagepipeline': 'facebook', 'com.facebook.cache': 'facebook', 'com.facebook.stetho': 'facebook', 'com.flurry.android': 'flurry', 'com.flurry.org': 'flurry', 'com.flurry.android.impl': 'flurry', 'com.sponsorpay.publisher': 'fyber', 'com.fyber.ads': 'fyber', 'com.fyber.mediation': 'fyber', 'com.fyber.c': 'fyber', 'com.sponsorpay.view': 'fyber', 'com.sponsorpay.mediation': 'fyber', 'com.sponsorpay.sdk.android': 'fyber', 'com.fyber.views': 'fyber', 'com.google.android.gms': 'google', 'com.google.firebase': 'google', 'com.startapp.android.publish': 'startapp', 'com.google.ads.mediation': 'google', 'com.google.ads': 'google', 'com.google.a': 'google', 'com.google.analytics': 'google', 'com.google.tagmanager': 'google', 'com.heyzap.sdk': 'heyzap', 'com.heyzap.house': 'heyzap', 'com.heyzap.mediation': 'heyzap', 'com.heyzap.common': 'heyzap', 'com.hyprmx.android': 'hyprmx', 'com.igaworks.gson': 'igaworks', 'com.igaworks.adbrix': 'igaworks', 'com.inmobi.commons': 'inmobi', 'com.inmobi.re': 'inmobi', 'com.inmobi.monetization.internal': 'inmobi', 'com.inmobi.signals': 'inmobi', 'com.inmobi.rendering': 'inmobi', 'com.inmobi.androidsdk': 'inmobi', 'com.supersonicads.sdk': 'ironsource', 'com.supersonic.mediationsdk': 'ironsource', 'com.supersonic.adapters': 'ironsource', 'me.kiip.internal': 'kiip', 'com.kochava.android': 'kochava', 'com.my.target': 'mail.ru', 'com.vk.sdk': 'mail.ru', 'com.mdotm.android': 'mdotm', 'com.milkmangames.extensions.android': 'milkman', 'com.milkmangames.extensions': 'milkman', 'com.millennialmedia.google.gson': 'millenialmedia', 'com.millennialmedia.internal': 'millenialmedia', 'com.millennialmedia.a': 'millenialmedia', 'com.mixpanel.android': 'mixpanel', 'com.moat.analytics.mobile.base': 'moat', 'com.adsdk.sdk': 'mobfox', 'com.mobvista.msdk': 'mobvista', 'com.skplanet.tad': 'mocomplex', 'com.mopub.mobileads': 'mopub', 'com.mopub.common': 'mopub', 'com.nativex.monetization': 'nativex', 'com.neatplug.u3d.plugins': 'neatplug', 'com.newrelic.agent.android': 'newrelic', 'org.nexage.sourcekit': 'nexage', 'org.nexage.sourcekit.mraid': 'nexage', 'com.bee7.gamewall': 'outfit7', 'com.bee7.sdk': 'outfit7', 'com.pingstart.adsdk': 'pingstart', 'com.playhaven.android': 'playhaven', 'io.presage.services': 'presage', 'io.presage.activities': 'presage', 'shared_presage.com.google': 'presage', 'shared_presage.com.google.gson': 'presage', 'io.presage.utils': 'presage', 'net.pubnative.library': 'pubnative', 'com.arellomobile.android.push': 'pushwoosh', 'com.revmob.ads': 'revmob', 'com.rfm.sdk': 'rubicon', 'com.sec.android.iap.lib': 'samsung', 'com.smaato.soma': 'smaato', 'com.smartadserver.android.library': 'smartadserver', 'com.swrve.sdk': 'swrve', 'com.tabtale.publishingsdk': 'tabtale', 'com.tabtale.mobile': 'tabtale', 'com.tapjoy.mraid': 'tapjoy', 'com.tencent.mm': 'tencent', 'com.tencent.open': 'tencent', 'com.tencent.connect': 'tencent', 'com.tencent.wxop.stat': 'tencent', 'com.tencent.stat': 'tencent', 'com.tnkfactory.framework': 'tnkfactory', 'com.tune.ma': 'tune', 'com.twitter.sdk.android': 'twitter', 'com.umeng.analytics': 'umeng', 'com.umeng.common': 'umeng', 'com.unity3d.player': 'unity', 'com.unity3d.ads.android': 'unitytechnologies', 'com.unity3d.ads': 'unitytechnologies', 'com.urbanairship.push': 'urbanairship', 'com.vungle.publisher': 'vungle', 'com.sina.weibo.sdk': 'weibo', 'com.yandex.metrica.impl': 'yandex', 'com.yandex.mobile.ads': 'yandex', 'com.yume.android': 'yume', 'com.zendesk.sdk': 'zendesk'}

statlib = json.load(open('../app-static-analysis/trie-5k.json'))
staturl  = json.load(open('200_mob_static_url.json'))
mobdyn = json.load(open('200_mob_dynamic_url.json'))
webdyn = json.load(open('200_web_dynamic_url.json'))

# map library package names to companies
for app in statlib:
	print app
	libcos = []
	for host in statlib[app]:
		if host in libtoco:
			lib = libtoco[host].title()
			libcos.append(lib)
		else:
			print 'no co found'
	libcos = list(set(libcos))
	statlib[app] = libcos




# select175 = []
# for app in select200:
# 	if app in statlib:
# 		select175.append(app)





# # remove outliers - tbc based on further manual analysis
# select175.remove('com.Time')
# select175.remove('com.huffingtonpost.android')

# get parents instead of children for each source:

def getParentCo(tracker):
	if tracker in obj:
		if (obj[tracker]['parent'] == ""):
			print 'no parent'
			return 0
		else:
			return obj[tracker]['parent']


for app in statlib:
	print statlib[app]
	for tracker in statlib[app]:
		print tracker
		parent = getParentCo(tracker)
		print parent
		if parent != 0:
			statlib[app].remove(tracker)
			statlib[app].append(parent)
	print statlib[app]

for app in staturl:
	print staturl[app]
	for tracker in staturl[app]:
		print tracker
		parent = getParentCo(tracker)
		print parent
		if parent != 0:
			staturl[app].remove(tracker)
			staturl[app].append(parent)
	print staturl[app]

for app in webdyn:
	print webdyn[app]
	for tracker in webdyn[app]:
		print tracker
		parent = getParentCo(tracker)
		print parent
		if parent != 0:
			webdyn[app].remove(tracker)
			webdyn[app].append(parent)
	print webdyn[app]

# compare webdyn vs mobstat
mobstat_unique_counts = []
webdyn_unique_counts = []
mobstat_webdyn_overlap_counts = []

select200 = []
for app in statlib:
	select200.append(app)

# get mappings for app name to website name
app_web_map = {"cc.dict.dictcc": "dict.cc", "com.dictionary": "dictionary.com", "com.dictionary.bn": "dictionary.com", "com.duckduckgo.mobile.android": "duckduckgo.com", "com.ebooks.ebookreader": "ebooks.com", "com.goodreads": "goodreads.com", "com.merriamwebster": "merriamwebster.com", "com.microsoft.bing": "bing.com", "com.oup.gab.odquicksearch": "en.oxforddictionaries.com", "com.scribd.app.reader0": "scribd.com", "com.tfd.mobile.TfdSearch": "tfd.com", "com.urbandictionary.android": "urbandictionary.com", "org.freedictionary": "freedictionary.org", "org.leo.android.dict": "leo.org", "org.wikipedia": "wikipedia.org", "com.cisco.webex.meetings": "webex.com", "com.citrix.saas.gotowebinar": "gotowebinar.com", "com.citrixonline.android.gotomeeting": "gotomeeting.com", "com.fiverr.fiverr": "fiverr.com", "com.indeed.android.jobsearch": "indeed.com", "com.jobkorea.app": "www.jobkorea.co.kr", "com.timesgroup.timesjobs": "www.timesjobs.com", "com.monster.android.Views": "monster.com", "naukriApp.appModules.login": "naukri.com", "net.infojobs.mobile.android": "infojobs.net", "net.slideshare.mobile": "slideshare.com", "com.crunchyroll.crmanga": "crunchyroll.com", "com.dccomics.comics": "dccomics.com", "com.marvel.comics": "marvel.com/comics", "jp.comico": "comico.jp", "com.cinemex": "cinemex.com", "com.eventbrite.attendee": "eventbrite.com", "com.imbc.mini": "imbc.com", "com.imdb.mobile": "imdb.com", "com.mobile.ign": "ign.com", "com.netflix.mediaclient": "netflix.com", "com.ninegag.android.app": "ninegag.com", "com.sonyliv": "sonyliv.com", "com.tudou.xoom.android": "tudou.com", "com.vimeo.android.videoapp": "vimeo.com", "com.wikia.singlewikia.gta": "wikia.com", "com.wwe.universe": "wwe.com", "de.tvspielfilm": "tvspielfilm.de", "fr.m6.m6replay": "m6.fr", "tv.pps.mobile": "pps.tv", "au.com.nab.mobile": "nab.com.au", "br.com.bb.android": "bancobrasil.com.br", "br.com.gabba.Caixa": "caixa.gov.br", "com.aastocks.dzh": "aastocks.com", "com.akbank.android.apps.akbank_direkt": "akbank.com", "com.bca": "bca.com", "com.bccard.mobilecard": "bccard.com", "com.bradesco": "bradesco.com", "com.garanti.cepsubesi": "garanti.com", "com.hanaskcard.app.touchstamp": "hanaskcard.com", "com.htsu.hsbcpersonalbanking": "hsbc.co.uk", "com.kbcard.cxh.appcard": "kbcard.com", "com.kbstar.kbbank": "kbstar.com", "com.paypal.android.p2pmobile": "paypal.com", "com.santander.app": "santander.com", "com.sbi.SBIFreedomPlus": "onlinesbi.com", "com.snapwork.hdfc": "hdfcbank.com", "com.vakifbank.mobile": "vakifbank.tr", "com.wf.wellsfargomobile": "wf.com", "com.wooribank.pib.smart": "wooribank.com", "com.wooricard.smartapp": "wooricard.com", "com.yahoo.mobile.client.android.finance": "finance.yahoo.com", "fr.creditagricole.androidapp": "creditagricole.fr", "gov.irs": "irs.gov", "info.percentagecalculator": "percentagecalculator.info", "pl.mbank": "mbank.pl", "ru.tcsbank.mcp": "tcsbank.ru", "se.bankgirot.swish": "bankgirot.se", "ua.privatbank.ap24": "privatbank.ua", "au.com.realestate.app": "realestate.com.au", "com.application.zomato": "www.zomato.com", "com.appsphere.innisfreeapp": "innisfree.co.kr", "com.aufeminin.marmiton.activities": "aufeminin.com", "com.cookpad.android.activities": "cookpad.com", "com.done.faasos": "done.com", "com.dubizzle.horizontal": "dubizzle.com", "com.frenys.verdadoreto": "frenys.com", "com.global.foodpanda.android": "foodpanda.com", "com.gumtree.android": "gumtree.com", "com.hotornot.app": "hotornot.com", "com.houzz.app": "houzz.com", "com.ikea.catalogue.android": "ikea.com", "com.inditex.pullandbear": "pullandbear.com", "com.inditex.zara": "zara.com", "com.kt.ollehfamilybox": "kt.com", "com.move.realtor": "move.com", "com.openrice.snap": "openrice.com", "com.redfin.android": "redfin.com", "com.restaurant.mobile": "restaurant.com", "com.rightmove.android": "rightmove.co.uk", "com.scripps.android.foodnetwork": "foodnetwork.com", "com.trulia.android": "trulia.com", "com.trulia.android.rentals": "trulia.com", "com.zoopla.activity": "zoopla.co.uk", "de.mcdonalds.mcdonaldsinfoapp": "mcdonalds.de", "de.pixelhouse": "pixelhouse.de", "ecowork.seven": "7-11.com", "fr.disneylandparis.android": "disneylandparis.fr", "jp.co.recruit.mtl.android.hotpepper": "hotpepper.jp", "kr.co.station3.dabang": "station3.co.kr", "com.AnatomyLearning.Anatomy3DViewer3": "AnatomyLearning.com", "com.anghami": "anghami.com", "com.bandsintown": "bandsintown.com", "com.gaana": "gaana.com", "com.gaana.oldhindisongs": "gaana.com", "com.jangomobile.android": "jango.com", "com.kugou.android": "kugou.com", "com.mixcloud.player": "mixcloud.com", "com.musixmatch.android.lyrify": "musixmatch.com", "com.spotify.music": "spotify.com", "com.vevo": "vevo.com", "de.radio.android": "radio.de", "uk.co.sevendigital.android": "7digital.com", "com.abc.abcnews": "abc.com", "com.andrewshu.android.reddit": "reddit.com", "com.backelite.vingtminutes": "20minutes.fr", "com.cnn.mobile.android.phone": "cnn.com", "com.dailymail.online": "dailymail.com", "com.elpais.elpais": "elpais.com", "com.et.reader.activities": "economictimes.indiatimes.com", "com.foxnews.android": "foxnews.com", "com.google.android.apps.genie.geniewidget": "news.google.com", "com.hespress.android": "hespress.com", "com.huffingtonpost.android": "huffingtonpost.com", "com.ideashower.readitlater.pro": "getpocket.com", "com.idmedia.android.newsportal": "dw.com", "com.indomedia.tabpulsa": "tabloidpulsa.co.id", "com.issuu.android.app": "issuu.com", "com.july.ndtv": "ndtv.com", "com.makonda.blic": "blic.rs", "com.mobilesrepublic.appy": "news-republic.com", "com.newspaperdirect.pressreader.android": "pressreader.com", "com.newspaperdirect.pressreader.android.hc": "pressreader.com", "com.nextmedia": "nextmedia.com", "com.nextmediatw": "nextmediatw.com", "com.nextradiotv.bfmtvandroid": "nextradiotv.com", "com.now.newsapp": "now.com", "com.nytimes.android": "nytimes.com", "com.sumarya": "alsumaria.tv/", "com.tilab": "virgilio.it/", "com.Time": "Time.com", "com.toi.reader.activities": "timesofindia.indiatimes.com", "com.usatoday.android.news": "usatoday.com", "com.zing.znews": "zing.vn", "com.zinio.mobile.android.reader": "zinio.com", "com.zumobi.msnbc": "ncbnews.com", "de.cellular.focus": "focus.de", "de.cellular.tagesschau": "tagesschau.de", "de.heute.mobile": "heute.de", "de.lineas.lit.ntv.android": "n-tv.de", "fr.lepoint.android": "lepoint.fr", "fr.playsoft.android.tv5mondev2": "tv5monde.com", "fr.playsoft.lefigarov3": "lefigaro.fr", "id.co.babe": "babe.co.id", "in.AajTak.headlines": "AajTak.in", "net.aljazeera.english": "aljazeera.net", "net.trikoder.android.kurir": "kurir.rs", "org.detikcom.rss": "detik.com", "ru.rian.reader": "ria.ru", "se.sr.android": "sverigesradio.se", "uk.co.economist": "www.economist.com", "blibli.mobile.commerce": "blibli.com", "br.com.dafiti": "dafiti.com.br", "com.acerstore.android": "acer.com", "com.alibaba.aliexpresshd": "aliexpress.com", "com.appnana.android.giftcardrewards": "appnana.com", "com.asda.android": "asda.com", "com.asos.app": "asos.com", "com.ebay.kleinanzeigen": "ebay-kleinanzeigen.de", "com.ebay.mobile": "ebay.com", "com.elevenst": "11st.co.kr", "com.elevenst.deals": "11st.co.kr", "com.etsy.android": "etsy.com", "com.flipkart.android": "flipkart.com", "com.geomobile.tiendeo": "tiendeo.co.za", "com.goldtouch.ct.yad2": "yad2.co.il", "com.groupon": "groupon.com", "com.hmallapp": "hmallapp.com", "com.hnsmall": "hnsmall.com", "com.homeshop18.activity": "homeshop18.com", "com.interpark.shop": "interpark.com", "com.jabong.android": "jabong.com", "com.lamoda.lite": "lamoda.com", "com.mercadolibre": "mercadolibre.com", "com.mobisoft.morhipo": "morhipo.com", "com.myntra.android": "myntra.com", "com.opensooq.OpenSooq": "opensooq.com", "com.sahibinden": "sahibinden.com", "com.shopclues": "shopclues.com", "com.shopping.limeroad": "limeroad.com", "com.shpock.android": "shpock.com", "com.snapdeal.main": "snapdeal.com", "com.souq.app": "souq.com"}

selectsub200 = []

for app in select200:
	if app in app_web_map:
		if app_web_map[app] in webdyn:
			selectsub200.append(app)

for app in selectsub200:
	statlib_trackers = statlib[app]
	staturl_trackers = staturl[app]
	mobstat_trackers = list(set(statlib_trackers).union(staturl_trackers))
	print mobstat_trackers
	website = app_web_map[app]
	webdyn_trackers = webdyn[website]
	mobstat_webdyn_overlap = len(set(mobstat_trackers).intersection(webdyn_trackers))
	mobstat_unique = len(set(mobstat_trackers) - set(webdyn_trackers))
	webdyn_unique = len(set(webdyn_trackers) - set(mobstat_trackers))
	mobstat_webdyn_overlap_counts.append(mobstat_webdyn_overlap)
	mobstat_unique_counts.append(mobstat_unique)
	webdyn_unique_counts.append(webdyn_unique)

print mobstat_unique_counts
print webdyn_unique_counts
print mobstat_webdyn_overlap_counts

print sum(mobstat_unique_counts)/float(len(mobstat_unique_counts))
print sum(webdyn_unique_counts)/float(len(webdyn_unique_counts))
print sum(mobstat_webdyn_overlap_counts)/float(len(mobstat_webdyn_overlap_counts))




# compare static (both url+library) to dynamic

# stat_dyn_overlap_counts = []
# dyn_unique_counts = []
# stat_unique_counts = []

# for app in select175:
# 	staturl_trackers = staturl[app]
# 	dyn_trackers = dyn[app]
# 	statlib_trackers = statlib[app]
# 	stat_trackers = list(set(statlib_trackers).union(staturl_trackers))
# 	print stat_trackers
# 	print dyn_trackers
# 	stat_dyn_overlap = len(set(stat_trackers).intersection(dyn_trackers))
# 	stat_unique = len(set(stat_trackers) - set(dyn_trackers))
# 	dyn_unique = len(set(dyn_trackers) - set(stat_trackers))
# 	stat_dyn_overlap_counts.append(stat_dyn_overlap)
# 	stat_unique_counts.append(stat_unique)
# 	dyn_unique_counts.append(dyn_unique)

# print dyn_unique_counts
# print stat_unique_counts
# print stat_dyn_overlap_counts

# print sum(dyn_unique_counts)/float(len(dyn_unique_counts))
# print sum(stat_unique_counts)/float(len(stat_unique_counts))
# print sum(stat_dyn_overlap_counts)/float(len(stat_dyn_overlap_counts))