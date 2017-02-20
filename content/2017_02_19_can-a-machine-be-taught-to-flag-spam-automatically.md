Title: Can a machine be taught to flag spam automatically
Date: 2017-2-19 22:51
Tags: Stack Exchange, machine learning, automation, programming
Category: Programming Projects
Slug: can-a-machine-be-taught-to-flag-spam-automatically
Summary: Description of how a group of people helped completely eliminate spam on the Stack Exchange network
Status: published

[TOC]

## Introduction

This is the draft version of a soon to go live Meta post. It will be updated here with the final version when that has
happened. 

---

TL;DR: [We][1] did it, so...yes.

---

## What is this?

Charcoal is the [organization][1] behind the [SmokeDetector][6] bot and other [nice things][5]. This bot scans new 
posts across the entire network for spam and reports it to various chatrooms where people can act on it. If a post has 
been created or edited, anywhere on the network, we've probably seen it. The bot utilizes our knowledge of how spammers 
work and what they have previously posted to come up with common patterns and rules to detect spam in the new and 
updated posts. You've likely seen the SmokeDetector bot if you visit chatrooms such as [Tavern on the Meta][2], 
[Charcoal HQ][3], [SO Close Vote Reviewers][4] and others across the network. Over time, the bot has become very 
accurate. 

Now we are leveraging the years of data and accuracy to automatically cast spam flags. With approximately 57,000 posts 
to draw from and over 45,000 true positives, we have a vast trove of data to utilize.

## What are we doing?

For over 3 years, SmokeDetector has reported potential spam so that users can flag the posts as appropriate. Users 
have provided feedback to inform the bot on whether the detection was correct or not (referred to as "feedback"). 
This feedback is stored in our web dashboard, [metasmoke][7] ([code][8]). Over time, we've used this feedback to 
evaluate our patterns ("reasons") and improve our accuracy. [Several][9] of our [reasons][10] are over 99.9% 
[accurate][11].

Early last year, and after getting a baseline accuracy from [jmac][12] (thank you!), we realized we could use the 
system to automatically cast spam flags. On Stack Overflow the current accuracy of users flagging spam posts is 85.7%. 
Across the rest of the network users are 95.4% accurate. We determined we can beat those numbers and eliminate spam 
from Stack Overflow and the rest of the network even faster. 

Without going into too much detail (if you really want it, it's available on our [website][13]), we leverage the 
accuracy of each existing reason to come up with a weight indicating how certain the system is that a post is spam. If 
this value exceeds a specific threshold, the system will cast up to three spam flags on the post. We cast multiple 
flags utilizing a number of different users' accounts and the Stack Exchange API. Via metasmoke, users are given the 
opportunity to [enable][14] their accounts to be used to flag spam. When a post is eligible for flagging because it 
exceeded the threshold set by each individual user, accounts are randomly selected from the pool of enabled users to 
cast a single flag each, up to a maximum of three per post so that we never unilaterally nuke something.

## What are our safety checks?

We designed the entire system with accuracy and sanity checks in mind. Our design collaborations are available for your 
browsing pleasure ([RFC 1][15], [RFC 2][16], [RFC 3][17]). The major things that make this system safe and sane are:

 - We give users a choice as to how accurate they want to be with their automatic flags. Before casting any flags, we 
 check that the preferences the user has set result in a spam detection accuracy of over 99.5% over a sample of at 
 least 1000 posts. Remember, on SO the current accuracy is 85.7% and network wide it is 95.4%. 
 - We do not unilaterally spam nuke a post, regardless of how sure we are it is spam. This means that a human *must* 
 be involved to finish off a post, even on the few sites with lower spam thresholds.
 - We’ve designed the system to be tolerant of faults - if there’s a malfunction anywhere in the system, any user with 
 access to SmokeDetector can immediately halt all automatic flagging - this includes all network moderators. If this 
 happens, it needs a system administrator to step in to re-enable flags.
 - We've discussed this with a community manager and have their [blessing][23] on the project.
 
## Results

We have been casting an average of 60-70 automatic flags per day for over two months, for a total of just over 3000 
flags network wide. These flags were cast by 22 different users. In that time, we've had [four][18]. We would be able 
to automatically cancel these particular cases, if there was a way to [retract flags via the API][22]. Since this is 
not possible, the flags are either declined by a moderator or manually retracted by the user.

[![Weights and Accuracy][19]][19]

The above graph plots the weight of the reasons against its overall volume of reports and accuracy. As minimum weight 
increases, accuracy (yellow line and rightmost Y-axis) and total reports (blue line) on the left-hand scale increase.

[![Automatic Flags per day][20]][20]

This shows the number of posts we've automatically flagged per day over the last month. The jump on February 15th, is 
due to increasing the number of automatic flags from 1 per post to 3 per post. You can see a live version of this graph 
on [metasmoke's autoflagging page][21]. There have been approximately 4,000 automatic spam flags cast, with only 3 
false positives.

[![Spam Hours][25]][25]

Spam arrives on Stack Overflow in waves. It is easy to see the time of day that many spam reports come in. The hours, 
above, are UTC time. The busiest spam times of day are the 8 hour block between 4am and Noon. We have affectionately 
named this "spam hour" in the chat room. 

[![Average Time to Deletion][24]][24]

Our goal is to delete spam quickly. The graph shows the time it takes for a reported spam post to be removed from the 
network. This section has three trend lines that show these averages. The first, red, section is when we were simply 
reporting the posts to chatrooms and all flags had to come from users. You can see we were are pretty constant in the 
time it takes to remove spam during this period. It took, on average, just over five minutes to get a post removed.

The green trend line is when we were issuing a single automatic flag. At implementation, we eliminated a full minute 
from time to deletion and after a month we'd eliminated two full minutes compared to no automatic flags.

The last section, the orange, is when we implemented three automatic flags to most sites. This was rolled out last
week, but it's already had a dramatic improvement on the time to deletion. We are seeing between 1 and 2 minutes to 
time to deletion versus the more than 3 minutes it was taking with only a single flag.

As mentioned above, spam arrives in waves. The dashed and dotted lines on the graph show the average deletion time 
during these two different time periods. The dashed lines show deletion time during 4am and Noon UTC, the dotted lines 
show the rest of the 24 hour period. An interesting thing this graph shows is that time to deletion during spam hour 
was higher when we didn't cast any automatic flags. It was removed faster outside of spam hour. That reversed when we 
started issuing a single auto-flag. The spam hour time to deletion is slightly lower than the average. Comparing the 
two time periods though, time to deletion during non-spam hour at the end of the non-flagging time period and the end 
of the single flag period are roughly the same.

## Discussion

We are confident in SmokeDetector and the three years of history it has. We've had many talented developers assist us 
over the years and many more users have provided feedback to improve our detection rules. Let us know what you want us 
to elaborate on, features you're wondering about or would like to see added, or things we might have missed in the 
process or the tooling. Take a look at the [feature][22] we'd really like Stack Exchange to consider so that we can 
further improve this system (and some of the other community built systems). We'll have [Charcoal members][1] hanging 
around and answering your questions. Alternatively, feel free to drop into [Charcoal HQ][3] and have a chat. 




 [1]: http://charcoal-se.org/people.html
 [2]: http://chat.meta.stackexchange.com/rooms/89/tavern-on-the-meta
 [3]: http://chat.stackexchange.com/rooms/11540/charcoal-hq
 [4]: http://chat.stackoverflow.com/rooms/41570/so-close-vote-reviewers
 [5]: https://github.com/Charcoal-SE
 [6]: https://github.com/Charcoal-SE/SmokeDetector
 [7]: https://metasmoke.charcoal-se.org
 [8]: https://github.com/Charcoal-SE/metasmoke
 [9]: https://metasmoke.erwaysoftware.com/reason/106
 [10]: https://metasmoke.erwaysoftware.com/reason/21
 [11]: https://metasmoke.erwaysoftware.com/reason/61
 [12]: http://stackoverflow.com/users/1933347/jmac
 [13]: https://charcoal-se.org/flagging
 [14]: https://metasmoke.erwaysoftware.com/flagging/preferences
 [15]: https://docs.google.com/document/d/1Bg0u4oY9W_skp79wSnyQWttUIBH8WV46JELDGJ7Bixo/edit
 [16]: https://docs.google.com/document/d/1voGyl3BUA1JHJ0pR2Mf9E5-wmIDUFC1G8HcThiS7B1k/edit
 [17]: https://docs.google.com/document/d/1Nu2U0uFbmHpb3v61WyBxjYNK34n5tFWAPYtvu13ZQCw/edit#heading=h.9nvcibv3gama
 [18]: https://metasmoke.erwaysoftware.com/flagging/logs?filter=fps
 [19]: {attach}images/spam-weights-and-accuracies.png
 [20]: {attach}images/spam-autoflags-per-day.png
 [21]: https://metasmoke.erwaysoftware.com/flagging
 [22]: http://meta.stackexchange.com/questions/288120/allow-retracting-flags-from-the-api
 [23]: http://chat.stackexchange.com/transcript/message/35437121#35437121
 [24]: {attach}images/spam-average-time-to-delete.png
 [25]: {attach}images/spam-spam-hours.png