import { flaskApi } from "lib/flaskApi";
import { getToken } from "next-auth/jwt";

export default async function usersHandler(req, res) {
  switch (req.method) {
    case "GET": {
      let accessToken = await getToken({
        req,
        secret: process.env.JWT_SECRET,
        raw: true,
      });
      let users = await flaskApi
        .getUsers({
          headers: { Authorization: `Bearer ${accessToken}` },
        })
        .catch((error) => {
          return { body: [] };
        });
      return res.json(users);
    }
  }
}
