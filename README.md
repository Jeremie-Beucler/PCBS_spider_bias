# Replicating the spider bias

## The project

>*Despite widespread claims to the contrary, the human mind is not worse than rational . . . but may often be better than rational.* (Cosmides and Tooby, 1994)

***


Tenants of evolutionary psychology have argued that **cognitive biases are not flaws, but often well-adapted features of organisms** who have faced the same problems in their environment throughout their evolutionary history. For instance, it may be advantageous to overdetect predators, whereas it is very costly to underdetect them. This is predicted by **Error Management Theory** (EMT; Haselton & Buss, 2000), which is an application of the Signal Detection Theory to cognitive mechanisms that include noise or incertitude and for which the costs of the type of error (i.e. false alarm or missed detection) are not equal.

In a 2013 article, Witt & Sugovic found that **we tend to inflate the speed of an approaching spider compared to a ball or a ladybug**; it may be adaptive as it increases our preparation time for action (e.g. fighting or fleeing).

![](results_witt.png)

*Results obtained by Witt & Sugovic, 2013*

I intend to replicate their experiment, with some minor changes:

- I won't implement their second factor, which was the size of the paddle used by the participants to block the incoming object (the threat to block and the size of the paddle acted independently from each other);
- in their experiment, they used a downwrd-facing projector to display the stimuli on a table; as I can't afford to use one, I will try to replicate the effect using a standard computer screen and Expyriment;
- in their experiment, they used a picture of a real spider; it may be interesting to **add some schematic representations of spiders to see if the bias is still there** (if it is, it may strenghtens the view that we possess some kind of "spider template", as found in infants by Rakison & Derringer, 2007);
- it may be interesting to **see if this effect is modulated by fear of spiders** (we may have chosen also age, psycho-social ressources, health, genre, and so forth).

To sum it up, in the present experiment, **participants will have to rate the speed of different objects coming towards them**. We expect **a main effect of Object type: the speed of the spider (real or schematic) will be inflated compared to other objects**.  We also expect **an interaction between Fear of spiders and Object type (the stronger the fear, the stronger the bias)**.

## Implementing the Fear of Spiders Qestionnaire

The *Fear of Spiders Questionnaire* (FSQ; Szymanksi & O’Donohue, 1995) contains 18 items, for which participants have to answer on a seven-point Likert scale. It has proven to be sensitive to non-phobic fears of spider (Muris & Merckelbach, 1996), which is the reason why I have decided to use it in my experiment. As I obviously don't want the participants to think the experiment is about spider fear, they will have to complete the questionnaire only after the speed evaluation process.

My goal is, for each question, to present the question (translated in french), and beneath it a seven-point scale, on which participants would have to click.There should also be a "Submit" button to go to the next question.
