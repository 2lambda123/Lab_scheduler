# Lab_scheduler
A combinatorial load-balancing scheduler for lab teaching at KTH.

At KTH, we used to assign PhD students to teaching slots manually (using Doodle). I wrote this script to automate this process, just for fun. The algorithm consists of three steps:

1) read individual input files in data folder (availability of the PhD students);
2) generate all the combinations; (Here, I applied a small trick: putting an upper limit of the number of combinations of each teaching day, otherwise the final combinations can be unbounded.)
3) evaluate the combinations based on working load and sort the final list.

In the original provided example, step 3) actually takes most of the time (a few seconds on my machine). It's expected since algorithm is almost brute-force. 
