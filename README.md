# Lab_scheduler
A combinatorial load-balancing scheduler for lab teaching at KTH.

At KTH, we used to assign PhD students to teaching slots manually (using Doodle). I wrote this script to automate this process, just for fun. The algorithm consists of three steps:

1) read individual input files in data folder (availability of the PhD students);
2) generate all the combinations; (Here, I applied a small trick: putting an upper limit of the number of combinations of each teaching day, otherwise the final combinations can be unbounded.)
3) evaluate the combinations based on working load and sort the final list.

In the original provided example, step 3) actually takes most of the time (a few seconds on my machine). It's expected since the algorithm is almost brute-force. 

## Cryptpad support

Cryptpad is a open-source, Google-free alternative which works as well as
Doodle. The functions provided in `src/cryptpad_schedule.py` can now be used
to process the options. The algorithm used is a mix of random-choice and
probabilistic approach to converge to a desired schedule. It works as follows:

1. Read the exported CSV file from a Cryptpad poll.
1. Iterate over each time slot and take into consideration the options `YES`
   and `MAYBE`. Give these options a fixed probability to start with say `80/20`.
1. Use `numpy.random.choice` to choose from the available TAs biased by the
   probability.
1. Skew the probability depending on the current assignments to balance the
   loads.
1. Iterate until a desired criteria is met.

Each iteration takes ~0.2 seconds on my machine.
