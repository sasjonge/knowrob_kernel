from ipykernel.kernelapp import IPKernelApp
from . import KnowRobKernel

IPKernelApp.launch_instance(kernel_class=KnowRobKernel)
