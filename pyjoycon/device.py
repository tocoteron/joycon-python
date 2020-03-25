import hid


def get_device_ids(debug=False):
    """
    returns dictionary of id info

    {
        "R": {
            "product": PRODUCT_ID,
            "vendor": VENDOR_ID
        },
        "L": {
            "product": PRODUCT_ID,
            "vendor": VENDOR_ID
        }
    }
    """
    devices = hid.enumerate(0, 0)
    R = {"vendor": None, "product": None}
    L = {"vendor": None, "product": None}

    for device in devices:
        prod = device['product_string']
        if prod and "Joy-Con" in prod:
            if debug:
                print(prod)
                print(f"product_id is {device['product_id']}")
                print(f"vendor_id is {device['vendor_id']}")

            if "R" in prod:
                R["product"] = device['product_id']
                R["vendor"] = device['vendor_id']
            else:
                L["product"] = device['product_id']
                L["vendor"] = device['vendor_id']
    return {"R": R, "L": L}


def get_ids(lr, **kw):
    """
    returns tuple of `(vendor_id, product_id)`

    arg: lr : str : put `R` or `L`
    """
    ids = get_device_ids(**kw)
    return (ids[lr]["vendor"], ids[lr]["product"])


def get_R_ids(**kw):
    """returns tuple of `(vendor_id, product_id)`"""
    return get_ids("R", **kw)


def get_L_ids(**kw):
    """returns tuple of `(vendor_id, product_id)`"""
    return get_ids("L", **kw)
