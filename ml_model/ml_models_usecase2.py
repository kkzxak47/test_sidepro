import os
from ml_model import TaskModel, basedir, db
from preload_models_usecase2 import blip_model, processor  # Import preloaded BLIP model and processor
from PIL import Image
from bson import ObjectId
import torch


# Use Case 2: Generate a description from an image
class GenerateDescriptionModel(TaskModel):
    def run(self):
        self.generate_description_task(self.message_data)

    def generate_description_task(self, data):
        # Save the uploaded image
        image_path = f"{data['task_id']}{data['ext']}"
        image_full_path = os.path.join(basedir, "static/descriptions_images", image_path)

        # Generate the caption
        caption = self.generate_caption(image_full_path)

        # Save the generated caption and image path in MongoDB
        self.update_task(data['task_id'], caption)

    def update_task(self, _id, caption):
        collection = db['generate-description']
        collection.update_one(
            {'_id': ObjectId(_id)},
            {'$set': {'caption': caption}}
        )

    def generate_caption(self, image_path):
        # Open the image, process it, and generate a caption
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        
        with torch.no_grad():
            outputs = blip_model.generate(
                **inputs,
                max_length=20,
                num_beams=5,
                repetition_penalty=2.0
            )
        
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        return caption
