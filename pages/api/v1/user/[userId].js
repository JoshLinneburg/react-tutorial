import { flaskApi } from "lib/flaskApi";
import { getToken } from "next-auth/jwt";

export default async function userHandler(req, res) {
  let { userId } = req.query;
  switch (req.method) {
    case "GET": {
      let accessToken = await getToken({
        req,
        secret: process.env.JWT_SECRET,
        raw: true,
      });

      let user = await flaskApi
        .getUserById(
          {
            headers: { Authorization: `Bearer ${accessToken}` },
          },
          userId
        )
        .catch((error) => {
          return { body: [] };
        });
      return res.json(user);
    }
  }
}
