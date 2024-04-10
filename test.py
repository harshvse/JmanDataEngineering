import requests
import csv
import os


def fetch_product_data(store_code, page=1, per_page=6):
    url = "https://locator-stores.lenskart.com/api/v3/store/inventory"
    payload = {
        "storeCode": store_code,
        "perPage": per_page,
        "page": page,
        "keyword": "",
    }
    headers = {
        "content-type": "application/json",
        "Xstoreaccesskey": "pNRq8BGvIHk/G9AwlBxKG5lz97eYDaxnWO0YYs+VrMY=",
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(response)
        return response.json()["data"]
    else:
        print("error")
        return None


def save_to_csv(store_code, products):
    filename = f"./data/{store_code}.csv"
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        for product in products:
            writer.writerow(
                [
                    product["store_code"],
                    product["product_id"],
                    product["quantity"],
                    product["price"],
                    product["product_name"],
                    product["brand"],
                    product["image_url"],
                    product["collection"],
                    product["product_url"],
                    product["gender"],
                    product["frame_material"],
                    product["frame_type"],
                    product["frame_size"],
                    product["frame_shape"],
                    product["frame_color"],
                    product["classification_name"],
                    product["stock_in_date"],
                    product["rr_30_days"],
                    product["rr_7_days"],
                    product["coco_qty"],
                    product["fofo_qty"],
                    ",".join(product["keywords"]),
                ]
            )


if __name__ == "__main__":
    with open(f"./store_codes.csv", mode="r") as codeFile:
        csvFile = csv.reader(codeFile)
        for lines in csvFile:
            for store_code in lines:
                filename = f"./data/{store_code}.csv"
                if not os.path.isfile(filename):
                    print(filename)
                    with open(filename, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            [
                                "store_code",
                                "product_id",
                                "quantity",
                                "price",
                                "product_name",
                                "brand",
                                "image_url",
                                "collection",
                                "product_url",
                                "gender",
                                "frame_material",
                                "frame_type",
                                "frame_size",
                                "frame_shape",
                                "frame_color",
                                "classification_name",
                                "stock_in_date",
                                "rr_30_days",
                                "rr_7_days",
                                "coco_qty",
                                "fofo_qty",
                                "keywords",
                            ]
                        )
                    page = 1
                    while True:
                        data = fetch_product_data(store_code, page)
                        if not data:
                            break

                        for product in data["data"]:
                            store_code = product["store_code"]
                            save_to_csv(store_code, [product])

                        if data["next_page_url"] is None:
                            break

                        page += 1
