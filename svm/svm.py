import matplotlib.pyplot as plt
import numpy as np 
import tensorflow as tf 
from sklearn import datasets

sess = tf.Session()

#load dataset
iris = datasets.load_iris()
x_vals = np.array([[x[0], x[3]]] for x in iris.data)
y_vals = np.array([1 if y == 0 else -1 for y in iris.target])

#get test and training datasets
train_indices = np.randomchoice(len(x_vals), round(len(x_vals)*0.8), replace = False)
test_indices = np.array(list(set(range(len(x_vals))) - set(train_indices)))
x_vals_train = x_vals[train_indices]
x_vals_test = x_vals[test_indices]
y_vals_train = y_vals[train_indeces]
y_vals_test = y_vals[test_indices]

#define module and loss function
batch_size = 100

#initial feedin
x_data = tf.placeholder(shape = [None, 3], dtype = tf.float32)
y_target = tf.placeholder(shape = [None, 1], dtype = tf.float32)

#new variable
A = tf.Variable(tf.random_normal(shape = [2, 1]))
b = tf.Variable(tf.random_normal(shape = [1, 1]))

#define linear module
model_output = tf.subtract(tf.matmul(x_data, A), b)

#declare vector L2 'norm' function squard
l2_norm = tf.reduce_sum(tf.square(A))

#loss = max(0, 1 - pred*actual) + alpha * l2_norm(A)^2
alpha = tf.constant([0.01])
classification_term = tf.reduce_mean(tf.maximum(0., tf.subtract(1., tf.multiply(model_output, y_target))))

loss = tf.add(classification_term, tf.multiply(alpha, l2_norm))

#start traing steps
my_opt = tf.train.GradientDescentOptimizer(0.01)
train_step = my_opt.minimize(loss)

init = tf.global_variables_initializer()
sess.run(init)

#training loop
loss_vec = []
train_accuracy = []
test_accuracy = []
for i in range(20000):
	rand_index = np.random.choice(len(x_vals_train), size = batch_size)
	rand_x = x_vals_train[rand_index]
	rand_y = np.transpose([y_vals_train[rand_index]])
	sess.run(train_step, feed_dict = {x_data: rand_x, y_target: rand_y})

#draw image
[[a1],[a2]] = sess.run(A)
[[b]] = sess.run(b)
slope = -a2/a1
y_intercept = b/a1
best_fit = []

x1_vals = [d[1] for d in x_vals]

for i in x1_vals:
	best_fit.append(slope*i + y_intercept)

#separate I. setosa
setosa_x = [d[1] for i, d in enumerate(x_vals) if y_vals[i] == 1]
setosa_y = [d[0] for i, d in enumerate(x_vals) if y_vals[i] == 1]
not_setosa_x = [d[1] for i, d in enumerate(x_vals) if y_vals[i] == -1]
not_setosa_y = [d[0] for i, d in enumerate(x_vals) if y_vals[i] == -1]

plt.plot(setosa_x, setosa_y, 'o', label = 'I.setosa')
plt.plot(not_setosa_x, not_setosa_y, 'x', label = 'Non-setosa')
plt.plot(x1_vals, best_fit, 'r-', label = 'Linear Separator', linewidth = 3)
plt.ylim([0, 10])
plt.legend(loc = 'lower right')
plt.title('Sepal Length vs Pedal Width')
plt.xlabel('Pedal Width')
plt.ylabel('Sepal Length')
plt.show()

