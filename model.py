import nengo
import matplotlib.pyplot as plt

model = nengo.Network()

with model:
    product_ensemble = nengo.Ensemble(n_neurons=40, dimensions=1)

    my_node = nengo.Node(output=0.5)

    nengo.Connection(my_node, product_ensemble)

    product_probe = nengo.Probe(product_ensemble, synapse=0.01)

sim = nengo.Simulator(model)

counter = 0

while counter < 1000:
    sim.step()
    counter = counter + 1
    print(counter)


print(sim.data[product_probe][-10:])

from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('multipage.pdf')

# Plot the decoded output of the ensemble
plt.plot(sim.trange(), sim.data[product_probe])
plt.xlim(0, 1)

plt.savefig(pp, format='pdf')

pp.close()