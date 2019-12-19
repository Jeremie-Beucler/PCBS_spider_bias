# Replicating the spider bias

>*Despite widespread claims to the contrary, the human mind is not worse than rational . . . but may often be better than rational.* (Cosmides and Tooby, 1994)

***

Tenants of evolutionary psychology have argued that **cognitive biases are not flaws, but often well-adapted features of organisms** who have faced the same problems in their environment throughout their evolutionary history. For instance, it may be advantageous to overdetect predators, whereas it is very costly to underdetect them. This is predicted by **Error Management Theory** (EMT; Haselton & Buss, 2000), which is an application of the Signal Detection Theory to cognitive mechanisms that include noise or incertitude and for which the costs of the type of error (i.e. false alarm or missed detection) are not equal.

In a 2013 article, Witt & Sugovic found that **we tend to inflate the speed of an approaching spider compared to a ball or a ladybug**; it may be adaptive as it increases our preparation time for action (e.g. fighting or fleeing).

![](results_witt.png)

*Results obtained by Witt & Sugovic, 2013*

I intend to replicate their experiment, with some minor changes:

- I won't implement their second factor, which was the size of the paddle used by the participants to block the incoming object (the threat to block and the size of the paddle acted independently from each other);
- in their experiment, they used a downward-facing projector to display the stimuli on a table; as I can't afford to use one, I will try to replicate the effect using a standard computer screen and Expyriment;
- in their experiment, they used a picture of a real spider; it may be interesting to **add some schematic representations of spiders to see if the bias is still there** (if it is, it may strenghtens the view that we possess some kind of "spider template", as found in infants by Rakison & Derringer, 2007), and to use other types of insect (which inspire disgust or not; which may harm us or not)
- it may be interesting to **see if this effect is modulated by fear of spiders**

To sum it up, in the present experiment, **participants will have to rate the speed of different objects coming towards them**. We expect **a main effect of Object type: the speed of the spider (real or schematic) will be inflated compared to other objects**.  We also expect **an interaction between Fear of spiders and Object type (the stronger the fear, the stronger the bias)**.

## How to run the project

1) Clone the repository on your computer using a terminal
2) Launch the program from your terminal: it takes two argument.

*E.g. if you want to compare the evaluation of the speed of a spider and of the speed of a fly, type:* "python Spider_bias.py tegenaria_domestica.png musca_domestica.png"

3) The data are stored in a *.xpd* file in the folder Data.

## Creating the stimuli

All the pictures were found on Google image and were free of rights. The logiciel [Gimp](https://www.gimp.org/fr/) was used to trim each picture from its background.

### Creating the background

As I could not use a downward-facing projector, I had to give the impression to the participant that he or she was looking down at the floor. In order to do that, I decided to create for each trial a [Canvas](https://docs.expyriment.org/expyriment.stimuli.Canvas.html) with a floor and the picture of neutral legs in blue jeans. 

![Background](background.png)

*The background on which the objects moved during the experiment*

### Finding the objects to animate

I decided to use different sorts of insects (e.g. dangerous or harmless ones, disgusting or not). The schematic spider drawings were found in the Material of Rakinson & Derringer (2007).

![](tegenaria_domestica.png)

*The picture of a spider used in the experiment ("Tegenaria domestica", the kind that hides in our basements in Europe)*

## Making the objects move

I needed, for each trial, to make the object move as if it were alive. I thus designed a function with its documentation.

```
def calc_pos(ancient_pos, verti_move, limit_verti):
	"""Defines the new position of a stimulus, whith a random horizontal movement and a fixed vertical one. 
	   When the stimulus crosses a fixed point on the y axis, the object makes a diagonal depending on which side
	   of the screen it was on the x axis.
	
	Args
	- ancient_pos(tuple): the previous position of the stimulus on the x and y axis
	- verti_move (int): the nb of pixel for the verti movement (i.e. the speed of the stimulus)
	- limit_verti (int): limit on the y axis for the stimulus to choose a side (left or right)
	
	Returns: the new position of the stimulus (tuple) and the degree of the rotation to apply to the stimulus (int)"""
  ```
  
At first, I tried to use the *"Move"* function of Expyriment, but I did not succeed to implement it on a Canvas so I decided to implement it directly in the function. 

The vertical move corresponds to the speed of the object, one of the variable of interest in the experiment. Thanks to the *random* function, I managed to give a random horizontal move to the stimuli (-5, 0 or 5), in order to make it look like it was moving on its own.

```
new_pos = [ancient_pos[0],(ancient_pos[1] + -1 * verti_move)]
	# translation du stimulus sur l'axe des y
	random_hori_move = random.randrange(-5,6,5)
```

The stimulus also had to rotate in the horizontal direction it was going to.

```
degree_rotation = random_hori_move
new_pos[0] += random_hori_move
```

The last block of code was used only if the stimulus was approaching the feet in the background picture; when it crosses the threshold, the stimulus chooses the side of the screen in which it was to move diagonally.

```
if new_pos[0] >= 0:
		# si le stimulus était dans la partie droite de l'écran
			new_pos[0] += 5 * (verti_move//5)
			#le stimulus part à droite
			degree_rotation = 7 + (verti_move//5)
else:
		# si le stimulus était dans la partie gauche de l'écran
			new_pos[0] += -1 * (5 * (verti_move//5))
			#le stimulus part à gauche
			degree_rotation = -7 - (verti_move//5)
```

And the function simply returns the new position of the object and the rotation to apply to it.

```return new_pos, degree_rotation```



## Implementing the Fear of Spiders Questionnaire

The *Fear of Spiders Questionnaire* (FSQ; Szymanksi & O’Donohue, 1995) contains 18 items, for which participants have to answer on a seven-point Likert scale. It has proven to be sensitive to non-phobic fears of spider (Muris & Merckelbach, 1996), which is the reason why I have decided to use it in my experiment. As I obviously don't want the participants to think the experiment is about spider fear, they will have to complete the questionnaire only after the speed evaluation process.

## What I learned from this course

### My previous coding experience

Before the course, I had followed a one-semester introductory course on Python. I thus knew the basics of the language (how to use a loop, how to build a function, and so forth), but I had never worked on a precise library before (such as Expyriment) nor had I written a full-scale functioning program.

### What I learned from this course

I feel like the course gave us a fantastic **toolbox** to use in our future projects: Pygame, Expyriment, Github, github.io, Pandas, the PCBS ressources and Automatetheboringstuff... Furthermore, we also learned about **good scientific practices**: the clarity of the code, the availability of the data and of the material used in the experiment (thanks to Github, for instance).

### What I still got to learn

I still have a lot to learn. For instance, I didn't used Expyriment in the most efficient way (I basically recoded the TouchScreenButtonBox as I didn't manage to use it whith a Canva object, and I didn't use the *"move"* function to move the stimuli). Also, my code could have shorter and clearer.

In the future, I would like to start using *R* for making statistics and get familiarized with Matlab. I also intend to deepen my knowledge in Python (finishing Automatetheboringstuff would be a good start).
