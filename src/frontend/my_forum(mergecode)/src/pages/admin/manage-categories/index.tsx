import { useEffect, useState } from "react";
import { requestGetAllCategories } from "../../../services/forum/get-all-categories";
import { CategoryFields } from "../../../services/forum/forum.client";
import { Model } from "../../../services/client";
import { Table, Button } from "@mantine/core";
import { format } from "date-fns";
import { requestDeleteCategory } from "../../../services/forum/delete-category";
import { Input, Pagination } from "@mantine/core";
import { IconAt, IconTrash } from "@tabler/icons-react";
import { requestCreateCategory } from "../../../services/forum/create-category";

const ManageCategories = () => {
  const [categories, setCategories] = useState<Model<CategoryFields>[]>([]);
  const [newCategoryName, setNewCategoryName] = useState("");
  const [currentPage, setCurrentPage] = useState<number>(1);
  const pageSize = 5;

  useEffect(() => {
    requestGetAllCategories()
      .then((categoriesResponse) => {
        setCategories(categoriesResponse.results);
      })
      .catch((error) => {
        console.error("Error fetching categories:", error);
      });
  }, []);

  const handleCreateCategory = () => {
    if (newCategoryName.trim() === "") {
      return;
    }

    const newCategoryData = { name: newCategoryName };

    requestCreateCategory(newCategoryData)
      .then((newCategory) => {
        setCategories([...categories, newCategory]);
        setNewCategoryName("");
      })
      .catch((error) => {
        console.error("Error creating category:", error);
      });
  };

  const handleDeleteCategory = (pk: number) => {
    requestDeleteCategory(pk)
      .then(() => {
        const updatedCategories = categories.filter(
          (category) => category.pk !== pk
        );
        setCategories(updatedCategories);
      })
      .catch((error) => {
        console.error("Error deleting category:", error);
      });
  };

  const columns = [
    { name: "pk", title: "ID" },
    { name: "name", title: "Name" },
    {
      name: "created",
      title: "Date created",
      render: (rowData: Model<CategoryFields>) =>
        format(new Date(rowData.fields.created), "MMMM dd, yyyy"),
    },
    {
      title: "Delete",
      render: (rowData: Model<CategoryFields>) => (
        <Button
          size="sm"
          variant="outline"
          color="red"
          onClick={() => handleDeleteCategory(rowData.pk)}
        >
          <IconTrash /> Delete
        </Button>
      ),
    },
  ];

  const totalCategories = categories.length;
  const totalPages = Math.ceil(totalCategories / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const visibleCategories = categories.slice(startIndex, startIndex + pageSize);

  return (
    <>
      <div className="mt-[20px] mb-[40px] flex items-center">
        <Input
          icon={<IconAt />}
          placeholder="New category"
          size="md"
          className="mr-[20px] w-[400px]"
          value={newCategoryName}
          onChange={(e) => setNewCategoryName(e.target.value)}
        />
        <Button variant="outline" color="blue" onClick={handleCreateCategory}>
          Create Category
        </Button>
      </div>

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
          {visibleCategories.map((category) => (
            <tr key={category.pk}>
              {columns.map((column) => (
                <td
                  key={column.name}
                  className={`px-4 py-2 ${
                    column.title === "Delete" ? "text-center" : ""
                  } ${column.title === "Date created" ? "text-center" : ""}`}
                >
                  {column.render
                    ? column.render(category)
                    : column.name === "pk" // Render pk explicitly
                    ? category.pk
                    : category.fields[column.name]}
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

export default ManageCategories;
