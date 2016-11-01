import got
from datetime import date
from datetime import timedelta
from time import strftime
from time import sleep
import shadowsocks

def crawl1DayTweet(f, currentDate):
	s = strftime("%Y-%m-%d", currentDate.timetuple())
	e = strftime("%Y-%m-%d", (currentDate + timedelta(1)).timetuple())
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('$aapl').setLang('en').setSince(s).setUntil(e).setMaxTweets(10000)
	tweets = got.manager.TweetManager.getTweets(tweetCriteria)
	if tweets == None:
		return False

	for t in reversed(tweets):
		f.write(t.id.encode('utf-8') + '\t' + t.username.encode('utf-8') + '\t' + str(t.date) + '\t' +
			t.geo.encode('utf-8') + '\t' + t.text.encode('utf-8') + '\t' + str(t.retweets) + '\t' + str(t.favorites)
			+ '\t' + t.hashtags.encode('utf-8') + '\t' + t.mentions.encode('utf-8') + '\t' + t.permalink.encode('utf-8') + '\n')
	return True

configs = [{'log-file': '/var/log/shadowsocks.log', 'localPort': 1080, 'local_port': 1080, 'shareOverLan': True, 'workers': 1, 'fast_open': False, 'timeout': 300, 'server': 'us01-54.ssv7.net', 'port_password': None, 'server_port': 24052, 'remarks': 'us01', 'local_address': '127.0.0.1', 'pid-file': '/var/run/shadowsocks.pid', 'password': 'USKjZVQyVNeS', 'method': 'aes-256-cfb', 'verbose': False}]

import sys
import os
import logging
import signal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from shadowsocks import shell, daemon, eventloop, tcprelay, udprelay, asyncdns

def deployProxy(configs, index):
	config = configs[index]
	try:
		logging.info("starting local at %s:%d" % (config['local_address'], config['local_port']))

		dns_resolver = asyncdns.DNSResolver()
		tcp_server = tcprelay.TCPRelay(config, dns_resolver, True)
		udp_server = udprelay.UDPRelay(config, dns_resolver, True)
		loop = eventloop.EventLoop()
		dns_resolver.add_to_loop(loop)
		tcp_server.add_to_loop(loop)
		udp_server.add_to_loop(loop)

		def handler(signum, _):
			logging.warn('received SIGQUIT, doing graceful shutting down..')
			tcp_server.close(next_tick=True)
			udp_server.close(next_tick=True)
		signal.signal(getattr(signal, 'SIGQUIT', signal.SIGTERM), handler)

		def int_handler(signum, _):
			sys.exit(1)
		signal.signal(signal.SIGINT, int_handler)

		daemon.set_user(config.get('user', None))
		loop.run()
	except Exception as e:
		raise

import multiprocessing
import random

if __name__ == '__main__':
	start_date = date(2015, 10, 1)
	end_date = date(2015, 10, 1)
	f = open('aapl-test-2', 'w')
	n = 0
	#index = random.randint(0, len(configs) - 1)
	index = 0
	while n <= int((end_date - start_date).days):
		#old_index = index
		#index = random.randint(0, len(configs) - 1)
		#while (index == old_index):
		#	index = random.randint(0, len(configs) - 1)
		single_date = start_date + timedelta(n)
		p = multiprocessing.Process(target = deployProxy, args = (configs, index))
		print('Using Proxy: %s' % configs[index]['remarks'])
		p.start()
		sleep(3)
		print("crawling %s..." % strftime("%Y-%m-%d", single_date.timetuple()))
		r = crawl1DayTweet(f, single_date)
		if r:
			print("%s done." % strftime("%Y-%m-%d", single_date.timetuple()))
			n += 1
		p.terminate()
	f.close()

