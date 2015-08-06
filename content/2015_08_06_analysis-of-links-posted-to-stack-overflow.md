Title: Analysis of links posted to Stack Overflow
Date: 2015-8-6 7:35
Tags: Stack Exchange, programming
Category: Side Activities
Slug: analysis-of-links-posted-to-stack-overflow
Summary: Approximately 10% of 1.5M randomly selected unique links in the Stack Overflow March 2015 data dump are unavailable. This is an analysis of how that was determined and a request for discussion on how to improve it
Status: published

[TOC]

TL;DR: Approximately 10% of 1.5M randomly selected unique links in the March 2015 [data dump][1] are unavailable. To be more precise, that is approximately 150K dead links.

---

## Motivation 

I've been running into more and more links that are dead on Stack Overflow and it's bothering me. In some cases, I've spent the time hunting down a replacement, in others I've notified the owner of the post that a link is dead, and (more shamefully), in others I've simply ignored it and left just a [down vote][2]. Obviously that's not good.

Before making sweeping generalizations that there are dead links everywhere, though, I wanted to make sure I wasn't just finding bad posts because I was wandering through the review queues. Utilizing the March 2015 data dump, I randomly selected about 25% of the posts (both questions and answers) and then parsed out the links. This works out to 5.6M posts out of 21.7M total.

Of these 5.6M posts, 2.3M contained links and 1.5M of these were unique links. I sent each unique URL a [`HEAD`][3] request, with a user agent mimicking Firefox<sup>1</sup>. I then retested everything that didn't return a successful response a week later. Finally, anything that failed from *that* batch, I resent a final test a week later. If a site was down in all three tests, I considered it down for this test.

--- 

## Results<sup>2</sup>

Good news/Bad News: A majority of the links returned a valid response, but there are still roughly 10% that failed.

[![PIE CHART IMAGE][status_image]][status_image]
*(This image is showing the top status codes returned)*

The three largest slices of the pie are the status 200s (site working!), status 404 (page not found, but server responded saying the page isn't found) and Connection Errors. Connection errors are sites that had no proper server response. The request to access the page timed out. I was generous in the time out and allowed a request to live for 20 seconds before failing a link with this status. The `4xx` and `5xx` errors are status codes that fall in the 400 and 500 range of HTTP responses. These are client and server error ranges, thus counted as a failure. `2xx` errors (of which was are in the low triple) are pages that responded with a success message in the 200 range, but it wasn't a `200` code. Finally, there were just over a hundred sites that hit a redirect loop that didn't seem to end. These are the `3xx` errors. I failed a site with this range if it redirected more than 30 times. There are a negligible number of sites that returned status codes in the 600 and [700][10] range<sup>4</sup>

There are, expectedly, many URLs that failed that appeared frequently in the sample set. Below is a list of the top 50<sup>3</sup> URLs that are in posts most often, but failed three times over the course of three weeks.

	http://docs.jquery.com/Plugins/validation
	http://www.eclipse.org/eclipselink/moxy.php
	http://jackson.codehaus.org/
	http://xstream.codehaus.org/
	http://opencv.willowgarage.com/wiki/
	http://developer.android.com/resources/articles/painless-threading.html
	http://valums.com/ajax-upload/
	http://sqlite.phxsoftware.com/
	http://qt.nokia.com/
	http://www.oracle.com/technetwork/java/codeconv-138413.html
	http://download.java.net/jdk8/docs/api/java/time/package-summary.html
	http://docs.oracle.com/javase/1.4.2/docs/api/java/text/SimpleDateFormat.html
	http://watin.sourceforge.net/
	http://leandrovieira.com/projects/jquery/lightbox/
	https://graph.facebook.com/
	https://ccrma.stanford.edu/courses/422/projects/WaveFormat/
	http://www.postsharp.org/
	http://www.erichynds.com/jquery/jquery-ui-multiselect-widget/
	http://ha.ckers.org/xss.html
	http://jetty.codehaus.org/jetty/
	http://cpp-next.com/archive/2009/08/want-speed-pass-by-value/
	http://codespeak.net/lxml/
	http://www.hpl.hp.com/personal/Hans_Boehm/gc/
	http://jquery.com/demo/thickbox/
	http://book.git-scm.com/5_submodules.html
	http://monotouch.net/
	http://developer.android.com/resources/articles/timed-ui-updates.html
	http://jquery.bassistance.de/validate/demo/
	http://codeigniter.com/user_guide/database/active_record.html
	http://www.phantomjs.org/
	http://watin.org/
	http://www.db4o.com/
	http://qt.nokia.com/products/
	http://referencesource.microsoft.com/netframework.aspx
	https://github.com/facebook/php-sdk/
	http://java.decompiler.free.fr/
	http://pivotal.github.com/jasmine/
	http://api.jquery.com/category/plugins/templates/
	http://code.google.com/closure/library
	http://www.w3schools.com/tags/ref_entities.asp
	http://xstream.codehaus.org/tutorial.html
	https://github.com/facebook/php-sdk
	http://download.java.net/maven/1/jstl/jars/jstl-1.2.jar
	https://developers.facebook.com/docs/offline-access-deprecation/
	http://www.parashift.com/c++-faq-lite/pointers-to-members.html
	https://developers.facebook.com/docs/mobile/ios/build/
	http://downloads.php.net/pierre/
	http://fluentnhibernate.org/
	http://net.tutsplus.com/tutorials/javascript-ajax/5-ways-to-make-ajax-calls-with-jquery/
	http://dev.iceburg.net/jquery/jqModal/


---
 
## Discussion

What can we do with all of this? How do we, as a community, solve the issue of 10% of our posts pointing to places on the internet that no longer exist? Assuming that my sample was indicative of the entire data dump, there are close to 600K (150K broken unique links x 4, because I took 1/4 of the data dump as a sample) broken links posted in questions and answers on Stack Overflow. I assume a large number of links posted in comments would be broken as well, but that's an activity for another month.

We encourage posters to provide snippets from their links just in case a link dies. That definitely helps, but the resources behind the links and the (presumably) expanded explanation behind the links are still gone. How can we properly deal with this? 

It looks like there have been a few previous discussions:

 - [Utilize the Wayback API to automatically fix broken links.][5] Development appeared to stall on this due to the large number of edits the Community user would be making. This would also hide posts that depended on said link from being surfaced for the community to fix it.
 - [Link review queue][6]. It was in [alpha][7], but disappeared in early 2014. 
 - [Badge proposal for fixing broken links][8]

---

## Footnotes

1. This is how it ultimately played out. Originally I sent `HEAD` requests, in an effort to save bandwidth. This turned out to waste a whole bunch of time because there are a whole bunch of sites around the internet that return a [`405 Method Not Allowed`][9] when sending a `HEAD` request. The next step was to sent `GET` requests, but utilize the default Python [requests][4] user-agent. A lot of sites were returning `401` or `404` responses to this user agent. 
2. Links to Stack Exchange sites were not counted in the above results. The failures seen are almost 100% due to a question/answer/comment being deleted. The process ran as an anonymous user, thus didn't have any reputation and was served a 404. A user with appropriate permissions *can* still visit the link. I verified a number of 404'd links to Stack Overflow posts and this was the case.
3. The 4th most common failure was to `localhost`. The 16th and 17th most common were `localhost` on ports other than 80. I removed these from the result table with the knowledge that these shouldn't be accessible from the internet.
4. There where 7 total URLs that returned status codes in the `600` and [`700`][10] range. One such site was [code.org][11] with a status code of 752. Sadly, this is not even defined the joke RFC. 


 [1]: https://archive.org/details/stackexchange
 [2]: http://meta.stackoverflow.com/a/262040/189134
 [3]: https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods
 [4]: http://docs.python-requests.org/en/latest/
 [5]: http://meta.stackexchange.com/a/198357/186281
 [6]: http://meta.stackexchange.com/questions/224895/what-happened-to-the-broken-link-review-queue
 [7]: http://meta.stackexchange.com/questions/212023/where-can-i-access-the-link-validation-review-queue
 [8]: http://meta.stackexchange.com/questions/174347/badge-request-for-fixing-dead-links-pipefitter
 [9]: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error
 [10]: https://github.com/joho/7XX-rfc
 [11]: http://learn.code.org/hoc/1
 [status_image]: {attach}images/status_codes.svg