import os
import csv
import numpy as np
from PIL import Image, ImageOps


def convert_images_to_csv(input_folder="my_numbers", output_csv="data/my_custom_dataset.csv"):
    # Open the new CSV file in write mode
    with open(output_csv, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        count = 0
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    img_path = os.path.join(input_folder, filename)
                    img = Image.open(img_path).convert('L')

                    img = ImageOps.invert(img)

                    img = img.resize((28, 28), Image.Resampling.LANCZOS)

                    pixel_array = np.array(img).flatten()

                    row = [""] + pixel_array.tolist()

                    writer.writerow(row)

                    print(f"Successfully processed: {filename}")
                    count += 1

                except Exception as e:
                    print(f"Skipped {filename}. Error: {e}")

        print(f"\nDone! Successfully converted {count} images and saved to {output_csv}.")


if __name__ == "__main__":
    convert_images_to_csv()