from diffusers import AmusedPipeline
from ml_model import TaskModel, basedir, db
from bson import ObjectId
import torch



# Use Case 1: Generate an image from a text prompt
class Text2ImageModel(TaskModel):
    def run(self):
        self.text2image_task(self.message_data)

    def update_task(self, _id, image_path):
        collection = db['text2image']
        result = collection.find_one({'_id': ObjectId(_id)})
        # write the name of the image to the database
        collection.update_one({'_id': ObjectId(_id)}, {'$set': {'image': image_path}})
        return result

    def text2image_task(self, data):
        # Load the model in fp32 precision (default for CPU)
        pipe = AmusedPipeline.from_pretrained(
            "amused/amused-256", torch_dtype=torch.float32
        )

        # Move the model to CPU
        pipe = pipe.to("cpu")

        # Define the prompt and negative prompt
        prompt = data['text']
        negative_prompt = ""

        # Generate the image on CPU
        image = pipe(prompt, negative_prompt=negative_prompt, generator=torch.manual_seed(0)).images[0]

        # Display or return the image
        image_path = f"{data['task_id']}.png"
        image.save(f"{basedir}/static/images/" + image_path)

        self.update_task(data['task_id'], image_path)
