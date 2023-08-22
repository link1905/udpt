import { Table, Text, Button } from "@mantine/core";
import React, { useEffect, useState } from "react";
import { requestGetAllThreads } from "../../../services/forum/get-all-thread";
import { requestDeleteThread } from "../../../services/forum/delete-thread";
import { requestUpdateThread } from "../../../services/forum/update-thread";
import { ThreadFields } from "../../../services/forum/forum.client";
import { Model } from "../../../services/client";
const ManageThreads = () => {
  const [threads, setThreads] = useState<Model<ThreadFields>[]>([]);
  const [approvedThreads, setApprovedThreads] = useState<{
    [key: number]: boolean;
  }>({});

  useEffect(() => {
    requestGetAllThreads()
      .then((threadsResponse) => {
        setThreads(threadsResponse.results);
      })
      .catch((error) => {
        console.error("Error fetching threads:", error);
      });
  }, []);
  useEffect(() => {
    const storedApprovedThreadsString = localStorage.getItem("approvedThreads");
    const storedApprovedThreads =
      storedApprovedThreadsString !== null
        ? JSON.parse(storedApprovedThreadsString)
        : {};
    setApprovedThreads(storedApprovedThreads);
  }, []);
  const handleDeleteThread = (pk: number) => {
    requestDeleteThread(pk)
      .then(() => {
        const updatedThreads = threads.filter((thread) => thread.pk !== pk);
        setThreads(updatedThreads);
      })
      .catch((error) => {
        console.error("Error deleting thread:", error);
      });
  };

  const handleEditStatus = (pk: number) => {
    const updatedApprovedThreads = { ...approvedThreads, [pk]: true };
    setApprovedThreads(updatedApprovedThreads);

    localStorage.setItem(
      "approvedThreads",
      JSON.stringify(updatedApprovedThreads)
    );

    const updateData = { approved: true };
    requestUpdateThread(pk, updateData)
      .then((updatedThread) => {
        console.log("Thread updated:", updatedThread);
      })
      .catch((error) => {
        console.error("Error updating thread:", error);
      });
  };

  const columns = [
    { name: "pk", align: "center", title: "ID" },
    { name: "title", title: "Title of thread" },
    { name: "content", title: "Content of thread" },
    {
      name: "approved",
      title: "Status",
      align: "center",
      render: (rowData: Model<ThreadFields>) => (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Text
            color={approvedThreads[rowData.pk] ? "green" : "red"}
            style={{ marginRight: "8px" }}
          >
            {approvedThreads[rowData.pk] ? "Approved" : "Not Approved"}
          </Text>
          <Button
            size="sm"
            variant="outline"
            color="blue"
            onClick={() => handleEditStatus(rowData.pk)}
            disabled={approvedThreads[rowData.pk]}
          >
            Edit
          </Button>
        </div>
      ),
    },

    {
      title: "Delete",
      render: (rowData: Model<ThreadFields>) => (
        <Button
          size="sm"
          variant="outline"
          color="red"
          onClick={() => handleDeleteThread(rowData.pk)}
        >
          Delete
        </Button>
      ),
    },
  ];

  return (
    <Table
      striped
      highlightOnHover
      withBorder
      withColumnBorders
      horizontalSpacing="xl"
      verticalSpacing="lg"
    >
      <thead>
        <tr>
          {columns.map((column) => (
            <th
              key={column.name}
              style={{
                textAlign: "center",
                color: "black",
                fontWeight: "bold",
              }}
            >
              {column.title || column.name}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {threads.map((thread) => (
          <tr key={thread.pk}>
            {columns.map((column) => (
              <td
                key={column.name}
                className={`px-4 py-2 ${
                  column.name === "pk" ||
                  column.title === "Status" ||
                  column.title === "Delete"
                    ? "text-center"
                    : ""
                }`}
              >
                {column.name === "title" ? (
                  thread.fields[column.name]
                ) : column.name === "content" ? (
                  <div
                    dangerouslySetInnerHTML={{
                      __html: thread.fields[column.name],
                    }}
                  />
                ) : column.render ? (
                  column.render(thread)
                ) : (
                  thread[column.name]
                )}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default ManageThreads;
