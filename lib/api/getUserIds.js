import axios from "axios";

export default async function getUserIds() {
  try {
    let response = await axios.get("http://localhost:5000/api/v1/user");
    return response.data.body.map((user) => user.public_id);
  } catch (error) {
    console.error(error);
  }
}
