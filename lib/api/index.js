import axios from "axios";

export class Api {
  constructor(config) {
    this.client = axios.create(config);
  }

  async getUsers() {
    let { data } = await this.client.get("/api/v1/user");
    return data.body;
  }

  async getUserById(publicId) {
    let { data } = await this.client.get(`/api/v1/user/${publicId}`);
    return data.body;
  }
}

export const api = new Api();

export function createServerSideApiClient(config = {}) {
  return new Api({ baseURL: "http://localhost:5000/", ...config });
}
