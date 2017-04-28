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

with open('200appsdynamic.csv') as f:
	reader = csv.reader(f)
	rows = list(reader)
select200 = []
for row in rows:
	select200.append(row[0])
select200 = list(set(select200))

statlib = json.load(open('../app-static-analysis/trie-5k.json'))
staturl  = json.load(open('200_mob_static_url.json'))
dyn = json.load(open('200_mob_dynamic_url.json'))

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

select175 = []
for app in select200:
	if app in statlib:
		select175.append(app)

# # remove outliers - tbc based on further manual analysis
# select175.remove('com.Time')
# select175.remove('com.huffingtonpost.android')

# get parents instead of children for each source:

# def getParentCo(tracker):
# 	if tracker in obj:
# 		if (obj[tracker]['parent'] == ""):
# 			print 'no parent'
# 			return 0
# 		else:
# 			return obj[tracker]['parent']

# for app in staturl:
# 	print staturl[app]
# 	for tracker in staturl[app]:
# 		print tracker
# 		parent = getParentCo(tracker)
# 		print parent
# 		if parent != 0:
# 			staturl[app].remove(tracker)
# 			staturl[app].append(parent)
# 	print staturl[app]

# for app in statlib:
# 	print statlib[app]
# 	for tracker in statlib[app]:
# 		print tracker
# 		parent = getParentCo(tracker)
# 		print parent
# 		if parent != 0:
# 			statlib[app].remove(tracker)
# 			statlib[app].append(parent)
# 	print statlib[app]

# for app in dyn:
# 	print dyn[app]
# 	for tracker in dyn[app]:
# 		print tracker
# 		parent = getParentCo(tracker)
# 		print parent
# 		if parent != 0:
# 			dyn[app].remove(tracker)
# 			dyn[app].append(parent)
# 	print dyn[app]

# compare static (both url+library) to dynamic

stat_dyn_overlap_counts = []
dyn_unique_counts = []
stat_unique_counts = []

for app in select175:
	staturl_trackers = staturl[app]
	dyn_trackers = dyn[app]
	statlib_trackers = statlib[app]
	stat_trackers = list(set(statlib_trackers).union(staturl_trackers))
	print stat_trackers
	print dyn_trackers
	stat_dyn_overlap = len(set(stat_trackers).intersection(dyn_trackers))
	stat_unique = len(set(stat_trackers) - set(dyn_trackers))
	dyn_unique = len(set(dyn_trackers) - set(stat_trackers))
	stat_dyn_overlap_counts.append(stat_dyn_overlap)
	stat_unique_counts.append(stat_unique)
	dyn_unique_counts.append(dyn_unique)

print dyn_unique_counts
print stat_unique_counts
print stat_dyn_overlap_counts

print sum(dyn_unique_counts)/float(len(dyn_unique_counts))
print sum(stat_unique_counts)/float(len(stat_unique_counts))
print sum(stat_dyn_overlap_counts)/float(len(stat_dyn_overlap_counts))