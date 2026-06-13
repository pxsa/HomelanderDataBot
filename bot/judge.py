TESTS = {
    # ---------------------------
    # Dataset & Split (20)
    # ---------------------------
    "test_dataset_count": {
        "expected": 50000,
        "score": 3,
        "message": "تعداد کل نمونه‌های دیتاست"
    },
    "test_train_count": {
        "expected": 40000,
        "score": 3,
        "message": "تعداد نمونه‌های Train"
    },
    "test_val_count": {
        "expected": 5000,
        "score": 2,
        "message": "تعداد نمونه‌های Validation"
    },
    "test_test_count": {
        "expected": 5000,
        "score": 2,
        "message": "تعداد نمونه‌های Test"
    },
    "test_split_seed": {
        "expected": 42,
        "score": 2,
        "message": "Seed تقسیم داده"
    },
    "test_n_samples": {
        "expected": 40000,
        "score": 3,
        "message": "تعداد نمونه‌های آماری"
    },
    "test_dataset_class_train_len": {
        "expected": 40000,
        "score": 2,
        "message": "طول Dataset آموزش"
    },
    "test_dataset_class_val_len": {
        "expected": 5000,
        "score": 2,
        "message": "طول Dataset اعتبارسنجی"
    },
    "test_dataset_class_test_len": {
        "expected": 5000,
        "score": 1,
        "message": "طول Dataset تست"
    },

    # ---------------------------
    # Transform & DataLoader (15)
    # ---------------------------
    "test_image_size": {
        "expected": 64,
        "score": 2,
        "message": "اندازه تصاویر"
    },
    "test_train_transform_names": {
        "expected": [
            "Resize",
            "RandomHorizontalFlip",
            "ToTensor"
        ],
        "score": 4,
        "message": "Transformهای Train"
    },
    "test_test_transform_names": {
        "expected": [
            "Resize",
            "ToTensor"
        ],
        "score": 2,
        "message": "Transformهای Test"
    },
    "test_train_flip_p": {
        "expected": 0.5,
        "score": 2,
        "tol": 1e-6,
        "message": "احتمال Flip"
    },
    "test_train_loader_shuffle": {
        "expected": True,
        "score": 2,
        "message": "Shuffle در TrainLoader"
    },
    "test_train_batches_count": {
        "expected": 625,
        "score": 1,
        "message": "تعداد Batchهای Train"
    },
    "test_val_batches_count": {
        "expected": 79,
        "score": 1,
        "message": "تعداد Batchهای Validation"
    },
    "test_test_batches_count": {
        "expected": 79,
        "score": 1,
        "message": "تعداد Batchهای Test"
    },

    # ---------------------------
    # Batch Statistics (15)
    # ---------------------------
    "test_batch_images_shape": {
        "expected": [64, 3, 64, 64],
        "score": 4,
        "message": "شکل Batch تصاویر"
    },
    "test_stats_shape": {
        "expected": [64, 3, 64, 64],
        "score": 2,
        "message": "شکل داده آماری"
    },
    "test_stats_min": {
        "expected": 0.0,
        "score": 2,
        "tol": 1e-6,
        "message": "کمینه پیکسل‌ها"
    },
    "test_stats_max": {
        "expected": 1.0,
        "score": 2,
        "tol": 1e-6,
        "message": "بیشینه پیکسل‌ها"
    },
    "test_global_mean": {
        "expected": [
            0.5163573026657104,
            0.41524842381477356,
            0.36230847239494324
        ],
        "score": 3,
        "tol": 1e-3,
        "message": "میانگین کانال‌های تصویر"
    },
    "test_global_std": {
        "expected": [
            0.2597065567970276,
            0.231986865401268,
            0.22424358129501343
        ],
        "score": 2,
        "tol": 1e-3,
        "message": "انحراف معیار کانال‌ها"
    },

    # ---------------------------
    # Model Architecture (30)
    # ---------------------------
    "test_total_params": {
        "expected": 2434243,
        "score": 12,
        "message": "تعداد پارامترهای مدل"
    },
    "ae_num_encoder_layers": {
        "expected": 12,
        "score": 6,
        "message": "تعداد لایه‌های Encoder"
    },
    "ae_num_decoder_layers": {
        "expected": 11,
        "score": 6,
        "message": "تعداد لایه‌های Decoder"
    },
    "ae_encoder_layer_types": {
        "expected": [
            "Conv2d",
            "BatchNorm2d",
            "ReLU",
            "Conv2d",
            "BatchNorm2d",
            "ReLU",
            "Conv2d",
            "BatchNorm2d",
            "ReLU",
            "Conv2d",
            "BatchNorm2d",
            "ReLU"
        ],
        "score": 3,
        "message": "ترتیب لایه‌های Encoder"
    },
    "ae_decoder_layer_types": {
        "expected": [
            "ConvTranspose2d",
            "BatchNorm2d",
            "ReLU",
            "ConvTranspose2d",
            "BatchNorm2d",
            "ReLU",
            "ConvTranspose2d",
            "BatchNorm2d",
            "ReLU",
            "ConvTranspose2d",
            "Sigmoid"
        ],
        "score": 3,
        "message": "ترتیب لایه‌های Decoder"
    },

    # ---------------------------
    # Training Results (20)
    # ---------------------------
    "test_plot_train_losses_length": {
        "expected": 5,
        "score": 2,
        "message": "تعداد نقاط Train Loss"
    },
    "test_plot_val_losses_length": {
        "expected": 5,
        "score": 2,
        "message": "تعداد نقاط Validation Loss"
    },
    "test_plot_train_loss_first": {
        "expected": 0.006399,
        "score": 4,
        "tol": 1e-4,
        "message": "Train Loss اولیه"
    },
    "test_plot_train_loss_last": {
        "expected": 0.005386,
        "score": 4,
        "tol": 1e-4,
        "message": "Train Loss نهایی"
    },
    "test_plot_val_loss_first": {
        "expected": 0.006603,
        "score": 4,
        "tol": 1e-4,
        "message": "Validation Loss اولیه"
    },
    "test_plot_val_loss_last": {
        "expected": 0.005333,
        "score": 4,
        "tol": 1e-4,
        "message": "Validation Loss نهایی"
    }
}


def is_equal(actual, expected, tol=1e-3):
    """
    Compare two values with support for:
    - float tolerance
    - list of floats
    - list of exact values
    """

    # float
    if isinstance(expected, float):
        return abs(actual - expected) <= tol

    # list
    if isinstance(expected, list):

        if not isinstance(actual, list):
            return False

        if len(actual) != len(expected):
            return False

        for a, e in zip(actual, expected):

            # list of floats
            if isinstance(e, float):
                if abs(a - e) > tol:
                    return False

            # list of exact values
            else:
                if a != e:
                    return False

        return True

    # bool, int, str ...
    return actual == expected


def judge(student_data):

    total_score = 0
    max_score = sum(
        test["score"]
        for test in TESTS.values()
    )

    report = []

    for key, test in TESTS.items():

        expected = test["expected"]
        score = test["score"]
        message = test.get("message", key)
        tol = test.get("tol", 1e-3)

        actual = student_data.get(key)

        # کلید وجود ندارد
        if actual is None:

            report.append(
                f"⚪ {message}\n"
                f"Missing ({key})\n"
                f"0/{score}"
            )

            continue

        # تست پاس شد
        if is_equal(actual, expected, tol):

            total_score += score

            report.append(
                f"✅ {message}\n"
                f"+{score}/{score}"
            )

        # تست رد شد
        else:

            report.append(
                f"❌ {message}\n"
                f"Expected: {expected}\n"
                f"Actual: {actual}\n"
                f"0/{score}"
            )

    return report, total_score, max_score