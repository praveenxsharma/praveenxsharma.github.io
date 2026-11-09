---
title: Harness2 by google is good , but who's gonna pay ?
date: 2026-11-09
tags:
  - "#Harness"
  - "#LLMs"
summary: Explaination and breakdown of harness2 by google for better understanding of mine
---
This blog breaks down harness2 paper by google , kind of like a summary or explanation according to my own understanding so it can be a lil biased  .

So let's begin with what this paper says ? , it uses a simple Propose-Probe-Compose Approach , what does the approach means ? , basically its what what we do everyday 
Does some task -> Fails -> retry with some another approach 

So google wants to automate this but with agents , google says as we were using harness up until now and modifying it manually to get better results such as a per project AGENTS.md file or your agent skills or some particular skills or just adding a one line instruction to write reports in your desired folder just to keep your files organized .

How we decide all this ? , me as a simple human i just see what my agent spending hours in (sometimes finding files from last session which it stored in /tmp or sometimes just writing reports in the project's directory which makes it even more frustrating ) , so i just mention these things in my global AGENTS.md which helps my agent to get some directions and this helps much more then expected , and this is what harness is the underlying skills, memory, tools, or sometimes just the subagents .

Now google wanting to automate this proposes two level of recursion one is task-level recursion and other one which modifies the general harness for future tasks , for example if we gave system a task to work on a legal document and it works with multiple parallel agent runs and comparing their output and then comparing those outputs and deciding which ones did better , but who's deciding ? for this paper we're leaving this on the model we are working with , and then rewriting the best harness according to the results but the issue is it only rewrote the tasks or harness just for that particular legal task , so if we give it a web application to debug now and once again another legal task , here the legal task will give better outcome as compared to the web application debug as it's improved and to solve this problem somewhat the paper introduces two different recursions one is task-level (it rewrites or appends improvements to the harness for current task) and other is the  harnessing level recursion (it modifies the general harness which helps in any type of task) .

But google had a lot of budget for this (they reech asf) . but neither do you , nor me
so who's gonna pay for those multiple parallel subagents ? 

the graph shows significant growth in benchmarks but do they really matter that much if the cost is growing same time exponentially for a task which you can do manually with some time and i don't mean that you doing those changes will give same growth as google's method but it won't be that bad too .

![[Pasted image 20261109123553.png|Benchmark scores: harness scaling gains +7.4 on Code, +8.4 on Web, +9.4 on Office over the base harness]]

overall a great research and great learning from this one to modify harness for our side .

you can read the whole paper [here](https://arxiv.org/pdf/2610.14224) 

~ Praveen Sharma 