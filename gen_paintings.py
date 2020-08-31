"""General-purpose test script for image-to-image translation.

See options/base_options.py and options/test_options.py for more test options.
See training and test tips at: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/tips.md
See frequently asked questions at: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/qa.md
"""
import os
from options.gen_options import GenOptions
from data import create_dataset
from models import create_model
from util.visualizer import save_images, save_images2
from util import html

# model_names = ["style_vangogh_pretrained", "style_monet_pretrained", "style_ukiyoe_pretrained"]
def run_style_transfer(filename):
    return run_pix2pix(filename)


def run_pix2pix(filename):
    opt = GenOptions().parse()
    # hard-code some parameters for test
    opt.num_threads = 0   # test code only supports num_threads = 1
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
    input_dir = os.path.dirname(filename)
    opt.dataroot = input_dir
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options)

    # create a website
    web_dir = os.path.join(input_dir, "output")  # define the website directory
    # web_dir = os.path.join(opt.results_dir, os.path.dirname(filename))  # define the website directory
    webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.epoch))

    for model_name in ["style_vangogh_pretrained", "style_monet_pretrained", "style_ukiyoe_pretrained"]:
        opt.name = model_name
        model = create_model(opt)      # create a model given opt.model and other options
        model.setup(opt)               # regular setup: load and print networks; create schedulers

        for i, data in enumerate(dataset):
            if i >= opt.num_test:  # only apply our model to opt.num_test images.
                break
            model.set_input(data)  # unpack data from data loader
            model.test()           # run inference
            visuals = model.get_current_visuals()  # get image results
            img_path = model.get_image_paths()     # get image paths
            save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize, model_name=model_name)
        webpage.save()  # save the HTML
    return web_dir

if __name__ == '__main__':
    run_pix2pix("input/golden_gate_bridge.jpg")