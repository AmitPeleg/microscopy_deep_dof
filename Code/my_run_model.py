import os
import argparse
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
import tensorflow as tf

import models.Reblur_model as model

is_parser = False

DATA_DIR = ''


def parse_args():
    if is_parser:
        parser = argparse.ArgumentParser(description='deblur arguments')
        parser.add_argument('--phase', type=str, default='test', help='determine whether train or test')
        parser.add_argument('--transfer_learning', type=bool, default=False)
        parser.add_argument('--datalist', type=str, default='./datalist_gopro.txt', help='training datalist')
        # parser.add_argument('--validationlist', type=str, default='./validation_set.txt')
        parser.add_argument('--model', type=str, default='color', help='model type: [lstm | gray | color]')
        parser.add_argument('--batch_size', help='training batch size', type=int, default=16)
        parser.add_argument('--epoch', help='training epoch number', type=int, default=200)
        parser.add_argument('--lr', type=float, default=1e-4, dest='learning_rate', help='initial learning rate')
        parser.add_argument('--gpu', dest='gpu_id', type=str, default='0', help='use gpu or cpu')
        parser.add_argument('--height', type=int, default=720,
                            help='height for the tensorflow placeholder, should be multiples of 16')
        parser.add_argument('--width', type=int, default=1280,
                            help='width for the tensorflow placeholder, should be multiple of-size 16 for 3 scales')
        parser.add_argument('--val_input_path', type=str, default='/opt/project/validation',
                            help='input path for validation images')
        parser.add_argument('--input_path', type=str, default='/opt/project/RealWorldScenes/Lab/OneShots',
                            help='input path for testing images')
        parser.add_argument('--output_path', type=str, default='/opt/project/test',
                            help='output path for testing images')
        parser.add_argument('--loaded_step', default=219000, type=int)

        args = parser.parse_args()

    else:
        args                   = type('args', (object,), {})()
        args.gpu_id            = '0'
        args.datalist          = '/opt/project/DataSet/ZEMAX_V2_2048.txt'
        args.transfer_learning = False
        args.model             = 'color'
        args.batch_size        = 16
        args.learning_rate     = 1e-4
        args.beta              = 0
        args.epoch             = 200
        args.expname           = 'test_for_git'
        args.upsample_type     = 'conv'
        args.val_input_path    = '/opt/project/validation'
        args.phase             = 'train'
        args.linear_data       = True
        args.crop_size         = 256
        args.normalize_noise   = False
        args.noise             = 'bpn_noise'
        args.n_levels          = 3
        # args.noise_std         = [0, 0.01, 0.05, 0.1] # Uniform noise
        args.noise_std         = [-3.5, -2., -3., -1.5]
        args.clip              = True
        args.org_ckpt_step     = 0
        args.step              = 0

        # testing
        # args.phase             = 'test'
        # args.step              = 220000
        args.height            = 720
        args.width             = 1280
        # args.expname           = 'test_the_code'
        # args.input_path        = '/opt/project/RealWorldScenes/Lab/OneShots'
        # args.output_path       = "/opt/project/RealWorldScenes/Lab/NewResults/{}/{}/".format(args.expname, args.step)
        # args.input_path        = '/opt/project/RealWorldScenes/UnderWater/OneShots'
        # args.output_path       = "/opt/project/RealWorldScenes/UnderWater/NewResults/{}/{}/".format(args.expname, args.step)


    args.restoring_same = True
    if args.upsample_type != 'conv' and args.step == 219000:
        args.restoring_same = False

    return args


def main(_):
    args = parse_args()

    # set gpu/cpu mode
    if int(args.gpu_id) >= 0:
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu_id
    else:
        os.environ['CUDA_VISIBLE_DEVICES'] = ''

    # set up deblur models
    deblur = model.DEBLUR(args)
    if args.phase == 'test':
        deblur.test(args.height, args.width, args.input_path, args.output_path)
    elif args.phase == 'train':
        deblur.train()
    else:
        raise IOError('phase should be set to either test or train')


if __name__ == '__main__':
    tf.compat.v1.app.run()
