import axios from "axios";

export class FlaskApi {
  constructor(config = {}) {
    this.client = axios.create({
      baseURL: process.env.FLASK_API_BASE_URL,
      ...config,
    });
  }

  async getUsers(config) {
    let response = await this.client.get("/api/v1/user", config);
    return response.data;
  }

  async getUserById(config, userId) {
    let response = await this.client.get(`/api/v1/user/${userId}`, config);
    return response.data;
  }
}

export const flaskApi = new FlaskApi();
