# ===========================================================================
#   classification.py -------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import shdw.__init__
import shdw.tools.data
import shdw.tools.imgtools
import shdw.tools.imagestats
import shdw.tools.welford
import shdw.tools.evaluation

import numpy as np

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_mlp_classification_stats(
    files, 
    specs,
    output,
    param_label=dict(),
    scale=100,
    param=dict(),

):
    shdw.__init__._logger.debug("Start creation of maximum likelihood classification map with settings:\n'specs':\t'{}',\n'output':\t'{}',\n'param_label':\t'{}',\n'scale':\t'{}',\n'param':\t'{}'".format(specs, output, param_label, scale, param))

    img_set_training, _ = shdw.tools.data.get_data(files, specs=specs, **output, scale=scale, param_label=param_label, show=False, live=True)

    # stats = [shdw.tools.welford.Welford()]*len(param_label)
    stats = [None]*len(param["channels"])
    for channel in range(len(param["channels"])):
        stats[channel] = [None]*len(param_label)
        for label in range(len(param_label)):
            stats[channel][label] = shdw.tools.welford.Welford()

    for item in iter(img_set_training):
        label_masks = shdw.tools.imgtools.get_label_mask(item[specs.index("label")].data, param_label.values())
        img = item[specs.index("msi")].data
        for channel in range(len(param["channels"])):
            for label in range(len(param_label.keys())):
                stats[channel][label].update(img[label_masks[...,label], channel])

    return stats

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_mlp_classification_map(
    stats,
    files, 
    specs,
    output,
    param_label=dict(),
    param_specs=list(),
    scale=100,
    param=dict(),
    log=None

):    
    img_set_test, save = shdw.tools.data.get_data(files, specs=specs, **output, scale=scale, param_label=param_label, show=False, live=True)

    eval_labeled_img = list()
    for channel in param["channels"]:
        eval_labeled_img.append(
            [
                shdw.tools.evaluation.EvalLabeledImg(list(param_label.values()), index=param_specs),
                shdw.tools.evaluation.ConfusionMap(list(param_label.values()), index=param_specs)            
            ]
        )

    for item in iter(img_set_test):
        labeled_img = get_labeled_img_from_stats_lut(
            stats, 
            item[specs.index("msi")].data
            # item[specs.index("msi")].data[..., param["channels"]]
        )

        save(item[0].path, shdw.tools.imgtools.project_data_to_img(labeled_img))
        label = item[specs.index("label")].data
        for count, channel in enumerate(param["channels"]):
            eval_labeled_img[count][0].update(labeled_img[...,channel], label)
            eval_labeled_img[count][1].update(labeled_img[...,channel], label)
    
    if log:
        with open(log, 'w+') as f:
            for count, channel in enumerate(param["channels"]):
                f.write("Classification report for channel '{}'\n{}\n\n".format(channel, eval_labeled_img[count][0].to_string()))

                f.write("Confusion Map for channel '{}'\n{}\n\n".format(channel, eval_labeled_img[count][1].to_string()))

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def new_mlp_mv_classification_map(
    stats,
    files, 
    specs,
    output,
    param_label=dict(),
    param_specs=list(),
    scale=100,
    param=dict(),
    log=None

):    
    img_set_test, save = shdw.tools.data.get_data(files, specs=specs, **output, scale=scale, param_label=param_label, show=False, live=True)

    eval_labeled_img = [
        shdw.tools.evaluation.EvalLabeledImg(list(param_label.values()), index=param_specs),
        shdw.tools.evaluation.ConfusionMap(list(param_label.values()), index=param_specs)            
    ]

    for item in iter(img_set_test):
        labeled_img = get_labeled_img_from_stats(
            stats, 
            item[specs.index("msi")].data
        )

        save(item[0].path, shdw.tools.imgtools.project_data_to_img(labeled_img))
        label = item[specs.index("label")].data

        eval_labeled_img[0].update(labeled_img, label)
        eval_labeled_img[1].update(labeled_img, label)
    
    if log:
        with open(log, 'w+') as f:
            f.write("Classification report for all channels '{}'\n{}\n\n".format(param["channels"], eval_labeled_img[0].to_string()))

            f.write("Confusion Map for all channels '{}'\n{}\n\n".format(param["channels"], eval_labeled_img[1].to_string()))

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_probability(mean, sd, values):
    var = 2*float(sd)**2
    if var:
        denom = (var*np.pi)**.5
        num = np.exp(-(values.astype(float)-float(mean))**2/var)
        return num/denom
    return np.zeros(len(values))

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_probability_scalar(mean, sd, value):
    var = 2*float(sd)**2
    if var:
        denom = (var*np.pi)**.5
        num = np.exp(-(float(value)-float(mean))**2/var)
        return num/denom
    return 0

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_prob(stats, values):
    prob_label = np.zeros((len(stats[0]), 1), dtype=float)
    for count_channel, channel_stats in enumerate(stats):
        for count_label, label_stats in enumerate(channel_stats):
            prob_label[count_label] += np.log(get_probability_scalar(
                    *label_stats.stats, values[count_channel]
                )
            )
    return np.argmax(prob_label, axis=0)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_lut(stats, values):
    lut_per_channel = np.zeros((len(values),len(stats)), dtype=float)
    for count, item in enumerate(stats):
        lut_per_channel[:, count] = get_probability(*stats[count].stats, values)
    
    return np.argmax(lut_per_channel, axis=1)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_lut_from_img(stats, img):
    return get_lut(stats, np.arange(np.min(img), np.max(img) + 1))

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_labeled_img_from_stats_lut(stats, img):
    img = shdw.tools.imgtools.expand_image_dim(img)
    
    img_labeled = np.ndarray(img.shape, dtype=np.uint8)
    for channel in range(img.shape[2]):

        try:
            stats_channel = stats[channel]
        except IndexError:
            stats_channel = stats[0]

        lut = get_lut_from_img(stats_channel, img=img[...,channel])
        img_labeled[...,channel] = lut[img[...,channel] - np.min(img[...,channel])]

    return img_labeled

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_labeled_img_from_stats(stats, img):
    img = shdw.tools.imgtools.expand_image_dim(img)
    
    img_labeled = np.ndarray(img.shape[0:-1], dtype=np.uint8)
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            img_labeled[row,col] = get_prob(stats, img[row, col, :])

    return img_labeled