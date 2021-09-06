import axios from "axios";
import { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import Table from "components/UserTable";

export default function Home() {
  let [users, setUsers] = useState([]);
  let [status, setStatus] = useState("loading");
  const columns = useMemo(
    () => [
      {
        Header: "First Name",
        accessor: "first_name",
      },
      {
        Header: "Last Name",
        accessor: "last_name",
      },
      {
        Header: "Email",
        accessor: "email",
      },
      {
        Header: "Phone Number",
        accessor: "phone_nbr",
      },
      {
        Header: "Links",
        accessor: "public_id",
        Cell(cell) {
          return (
            <span>
              <Link href={`/user/${cell.value}?editing=false`}>
                <a>View</a>
              </Link>
              <span> or </span>
              <Link href={`/user/${cell.value}?editing=true`}>
                <a>Edit</a>
              </Link>
            </span>
          );
        },
      },
    ],
    []
  );

  useEffect(() => {
    async function getData() {
      try {
        let response = await axios.get("/api/v1/user");
        setUsers(response.data.body);
        setStatus("success");
      } catch (error) {
        setStatus("error");
        console.error(error);
      }
    }
    if (status === "loading") {
      getData();
    }
  }, []);

  return (
    <div>
      {status === "success" ? (
        <>
          <Table columns={columns} data={users} />
        </>
      ) : (
        "Loading..."
      )}
    </div>
  );
}
