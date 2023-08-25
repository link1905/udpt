import React, { useState, useEffect } from "react";
import { requestGetThread } from "../services/forum/get-thread";
import { requestGetCategory } from "../services/forum/get-category";
function ThreadDetail({ threadId }) {
  const [thread, setThread] = useState(null);
  const [category, setCategory] = useState(null);

  useEffect(() => {
    // Gọi API để lấy thông tin thread
    requestGetThread(threadId)
      .then((threadData) => {
        setThread(threadData);
        // Sau khi có thông tin thread, gọi API để lấy thông tin category
        return requestGetCategory(threadData.fields.category.pk);
      })
      .then((categoryData) => {
        setCategory(categoryData.fields.name);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, [threadId]);

  return (
    <div>
      {/* Hiển thị thông tin của thread */}
      {thread && (
        <div>
          <h1>{thread.fields.title}</h1>
          <p>{thread.fields.content}</p>
          <p>Category: {category}</p> {/* Hiển thị tên category */}
          {/* ... Hiển thị các thông tin khác của thread */}
        </div>
      )}
    </div>
  );
}

export default ThreadDetail;
