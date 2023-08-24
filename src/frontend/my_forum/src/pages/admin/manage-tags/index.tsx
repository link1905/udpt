import { useEffect, useState } from "react";
import { requestGetAllTags } from "../../../services/tag/get-all-tags";
import { requestDeleteTag } from "../../../services/tag/delete-tag";
import { TagFields } from "../../../services/tag/tag.client";
import { Model } from "../../../services/client";
import {
  Table,
  Button,
  Pagination,
  Input,
  Modal,
  Paper,
  Text,
} from "@mantine/core";
import { requestCreateTag } from "../../../services/tag/create-tag";
const ManageTags = () => {
  const [tags, setTags] = useState<Model<TagFields>[]>([]);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const pageSize = 5;
  const [newTagName, setNewTagName] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    requestGetAllTags()
      .then((tagsResponse) => {
        setTags(tagsResponse.results);
      })
      .catch((error) => {
        console.error("Error fetching tags:", error);
      });
  }, []);

  const handleDeleteTag = (pk: number) => {
    requestDeleteTag(pk)
      .then(() => {
        const updatedTags = tags.filter((tag) => tag.pk !== pk);
        setTags(updatedTags);
      })
      .catch((error) => {
        console.error("Error deleting tag:", error);
      });
  };

  const handleCreateTag = () => {
    if (newTagName.trim() === "") {
      return;
    }

    const newTagData = { name: newTagName };

    requestCreateTag(newTagData)
      .then((newTag) => {
        setTags([...tags, newTag]);
        setNewTagName("");
        setIsModalOpen(false);
      })
      .catch((error) => {
        console.error("Error creating tag:", error);
      });
  };

  const columns = [
    { name: "name", title: "Name" },
    {
      title: "Delete",
      render: (rowData: Model<TagFields>) => (
        <Button
          size="sm"
          variant="outline"
          color="red"
          onClick={() => handleDeleteTag(rowData.pk)}
        >
          Delete
        </Button>
      ),
    },
  ];

  const totalTags = tags.length;
  const totalPages = Math.ceil(totalTags / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const visibleTags = tags.slice(startIndex, startIndex + pageSize);

  return (
    <>
      <div className="mt-[20px] mb-[40px] flex items-center">
        <Button
          variant="outline"
          color="blue"
          onClick={() => setIsModalOpen(true)}
        >
          Create Tag
        </Button>
      </div>
      <Modal
        title="Create New Tag"
        size="xs"
        opened={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      >
        <Paper padding="lg" >
          <Input
            placeholder="Tag Name"
            value={newTagName}
            onChange={(e) => setNewTagName(e.target.value)}
          />
          <Button
            color="blue"
            style={{ marginTop: "10px" }}
            onClick={handleCreateTag}
            className="bg-blue-500 text-white border-blue-500 ml-[100px] "
          >
            Create
          </Button>
        </Paper>
      </Modal>
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
          {visibleTags.map((tag) => (
            <tr key={tag.pk}>
              {columns.map((column) => (
                <td
                  key={column.name}
                  className={`px-4 py-2 ${
                    column.title === "Delete" ? "text-center" : ""
                  }`}
                >
                  {column.render ? column.render(tag) : tag.fields[column.name]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </Table>

      <Pagination
        className="justify-center mt-[40px]"
        total={totalPages}
        value={currentPage}
        onChange={setCurrentPage}
      />
    </>
  );
};

export default ManageTags;
